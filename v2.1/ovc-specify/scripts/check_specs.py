#!/usr/bin/env python3
"""OVC Framework v2 spec checker.

Plain Python 3.8+, standard library only.

Usage:
  python3 check_specs.py --brief project-brief.md
  python3 check_specs.py --root . [--brief docs/project-brief.md]
                         [--track lite|standard|full] [--docs-dir docs]
                         [--allow-open-questions]
  python3 check_specs.py --root . --mode brownfield

Exit codes:
  0  all checks passed
  1  one or more checks failed
  2  brief rejected (unknown or missing version, bad track) or bad usage
"""

import argparse
import re
import sys
from pathlib import Path

SUPPORTED_BRIEF_VERSIONS = {2}
TRACKS = ("lite", "standard", "full")
LEVELS = ("beginner", "intermediate", "expert")
DEFAULT_LEVEL = {"lite": "beginner", "standard": "intermediate", "full": "intermediate"}
STATUSES = {
    "planned": "Planned",
    "mitigated": "Mitigated",
    "accepted risk": "Accepted risk",
    "open": "Open",
}
BRIEF_SECTIONS = [
    "problem",
    "users",
    "scope",
    "success looks like",
    "constraints",
    "performance & efficiency goals",
    "key decisions",
    "builder & learning goals",
    "security & privacy concerns",
    "assumptions & risks",
    "open questions",
    "raw notes",
]
PLACEHOLDERS = {"", "-", "--", "\u2014", "\u2013", "tbd", "todo", "?", "...", "none", "n/a", "na", "x"}
EVIDENCE_RE = re.compile(r"^(test|scan|manual)\s*:\s*\S", re.I)
REQ_ID_RE = re.compile(r"\b(?:FR|NFR)-\d{3}\b")
REQ_DEF_RE = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+|\|\s*)\**\s*((?:FR|NFR)-\d{3})\b")
OQ_RE = re.compile(r"\[OPEN QUESTION\b", re.I)
FENCE_RE = re.compile(r"^\s*(```|~~~)")


class Report:
    def __init__(self):
        self.fails = []
        self.warns = []

    def fail(self, where, msg):
        self.fails.append((where, msg))

    def warn(self, where, msg):
        self.warns.append((where, msg))

    def print(self):
        for where, msg in self.fails:
            print("FAIL  %s: %s" % (where, msg))
        for where, msg in self.warns:
            print("WARN  %s: %s" % (where, msg))
        if self.fails:
            print("\nRESULT: FAIL (%d failure(s), %d warning(s))" % (len(self.fails), len(self.warns)))
        else:
            print("\nRESULT: PASS (%d warning(s))" % len(self.warns))


# ----------------------------------------------------------------- helpers

def read_text(path):
    return Path(path).read_text(encoding="utf-8-sig")


def strip_md(s):
    s = s.replace("\\|", "|")
    s = re.sub(r"[*`_]", "", s)
    return s.strip()


def is_placeholder(s):
    return strip_md(s).lower() in PLACEHOLDERS


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def is_separator(cells):
    return bool(cells) and all(re.match(r"^:?-{2,}:?$", c.strip()) for c in cells)


def parse_tables(text):
    """Return a list of tables: {'header': [lowercased cells], 'rows': [(lineno, cells)]}.
    Tables inside fenced code blocks are ignored."""
    lines = text.splitlines()
    tables = []
    cur = None
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            cur = None
            i += 1
            continue
        if in_fence or not line.strip().startswith("|"):
            cur = None
            i += 1
            continue
        if cur is None:
            header = split_row(line)
            if i + 1 < len(lines) and is_separator(split_row(lines[i + 1])):
                cur = {"header": [strip_md(h).lower() for h in header], "rows": []}
                tables.append(cur)
                i += 2
                continue
            i += 1
            continue
        cells = split_row(line)
        n = len(cur["header"])
        cells = (cells + [""] * n)[:n] if len(cells) < n else cells
        cur["rows"].append((i + 1, cells))
        i += 1
    return tables


def col(header, *needles):
    for idx, h in enumerate(header):
        if any(n in h for n in needles):
            return idx
    return None


def lines_outside_fences(text):
    in_fence = False
    for no, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield no, line


def parse_front_matter(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if m:
            meta[m.group(1).lower()] = m.group(2).strip().strip("\"'")
    return None  # header never closed


# ------------------------------------------------------------ brief check

def check_brief(path):
    """Return (exit_code, track_or_None, level_or_None, messages)."""
    p = Path(path)
    if not p.is_file():
        return 2, None, None, ["Brief not found: %s" % path]
    text = read_text(p)
    meta = parse_front_matter(text)
    if meta is None:
        return 2, None, None, [
            "No OVC header found at the top of %s." % path,
            "This looks like a v1 brief (or not a brief). ovc-specify v2 reads version 2 only.",
            "Offer the person an upgrade: ask the track, add the header "
            "(ovc-brief-version: 2, track, project), and add the new sections "
            "'Success looks like' and 'Assumptions & risks'. Save only after they approve.",
        ]
    ver = meta.get("ovc-brief-version")
    if ver is None:
        return 2, None, None, [
            "The header has no 'ovc-brief-version' key.",
            "This looks like a v1 brief. See the upgrade steps in ovc-specify Step 1.",
        ]
    try:
        ver_int = int(ver)
    except ValueError:
        ver_int = None
    if ver_int not in SUPPORTED_BRIEF_VERSIONS:
        return 2, None, None, [
            "Unsupported ovc-brief-version: %r. This skill reads version(s) %s only. "
            "Stop and tell the person; do not guess a conversion."
            % (ver, ", ".join(str(v) for v in sorted(SUPPORTED_BRIEF_VERSIONS)))
        ]
    track = meta.get("track", "").lower()
    if track not in TRACKS:
        return 2, None, None, [
            "Invalid or missing 'track': %r. It must be exactly one of: %s." % (meta.get("track"), ", ".join(TRACKS))
        ]
    level = meta.get("level", "").lower()
    if meta.get("level") is not None and level not in LEVELS:
        return 2, None, None, [
            "Invalid 'level': %r. It must be one of: %s (or omit it)." % (meta.get("level"), ", ".join(LEVELS))
        ]
    if not level:
        level = DEFAULT_LEVEL[track]
    msgs = []
    if not meta.get("project"):
        msgs.append("WARN header has no 'project' name.")
    headings = [strip_md(re.sub(r"^#+\s*", "", ln)).lower() for ln in text.splitlines() if ln.startswith("#")]
    for sec in BRIEF_SECTIONS:
        if not any(h.startswith(sec) for h in headings):
            msgs.append("WARN brief is missing the section '%s'." % sec)
    return 0, track, level, msgs


# --------------------------------------------------------------- checkers

def check_open_questions(files, rep, allow):
    for f in files:
        if not f.is_file():
            continue
        for no, line in lines_outside_fences(read_text(f)):
            line_wo_code = re.sub(r"`[^`]*`", "", line)
            if OQ_RE.search(line_wo_code):
                msg = "unresolved open question: %s" % line.strip()[:140]
                (rep.warn if allow else rep.fail)("%s:%d" % (f.name, no), msg)


def requirement_defs(text):
    """Return {id: (lineno, requirement_text, row_cells_or_None)}; duplicates reported by caller."""
    defs = {}
    dups = []
    tables = parse_tables(text)
    table_rows = {}
    for t in tables:
        for no, cells in t["rows"]:
            table_rows[no] = (t, cells)
    for no, line in lines_outside_fences(text):
        m = REQ_DEF_RE.match(line)
        if not m:
            continue
        rid = m.group(1)
        if no in table_rows:
            t, cells = table_rows[no]
            body = cells[1] if len(cells) > 1 else ""
        else:
            body = line[m.end():]
        if rid in defs:
            dups.append((rid, no))
        else:
            defs[rid] = (no, body, table_rows.get(no))
    return defs, dups


def check_status_table(sec_path, rep, track):
    """Validate the STRIDE table in SECURITY.md (Standard/Full/brownfield)."""
    name = sec_path.name
    tables = parse_tables(read_text(sec_path))
    cands = []
    for t in tables:
        h = t["header"]
        if col(h, "status") is not None and col(h, "verified") is not None:
            cands.append(t)
    if not cands:
        rep.fail(name, "no threat table with 'Status' and 'Verified by' columns found")
        return
    total_rows = 0
    for t in cands:
        h = t["header"]
        c_status = col(h, "status")
        c_ver = col(h, "verified")
        c_mit = col(h, "mitigation")
        for no, cells in t["rows"]:
            if all(not strip_md(c) for c in cells):
                continue
            total_rows += 1
            where = "%s:%d" % (name, no)
            raw_status = strip_md(cells[c_status]).lower()
            if not raw_status:
                rep.fail(where, "threat row has no status (use Planned, Mitigated, Accepted risk, or Open)")
                continue
            if raw_status not in STATUSES:
                rep.fail(where, "unknown status %r (allowed: Planned, Mitigated, Accepted risk, Open)" % cells[c_status])
                continue
            status = STATUSES[raw_status]
            evidence = strip_md(cells[c_ver])
            if status == "Mitigated":
                if not EVIDENCE_RE.match(evidence):
                    rep.fail(where, "'Mitigated' needs typed evidence in 'Verified by' "
                                    "(test: ..., scan: ..., or manual: ...); found %r" % evidence)
            elif status == "Planned":
                if is_placeholder(evidence):
                    (rep.fail if track == "full" else rep.warn)(
                        where, "'Planned' row should name the planned check in 'Verified by'")
            elif status == "Accepted risk":
                reason = strip_md(cells[c_mit]) if c_mit is not None else ""
                if is_placeholder(reason) and is_placeholder(evidence):
                    rep.warn(where, "'Accepted risk' should state who accepted it and why")
    if total_rows == 0:
        rep.fail(name, "threat table has no rows; list the threats or write them as Accepted risk with a reason")


def check_trace(spec_path, plan_path, track, rep):
    """Every requirement ID in the PRD/SPEC must be traced to a phase and a typed check."""
    spec_text = read_text(spec_path)
    defs, dups = requirement_defs(spec_text)
    for rid, no in dups:
        rep.fail("%s:%d" % (spec_path.name, no), "duplicate requirement ID %s" % rid)
    if not defs:
        rep.fail(spec_path.name, "no requirement IDs found (expected rows or bullets starting with FR-001, NFR-001, ...)")
        return defs

    nfrs = [(rid, v) for rid, v in defs.items() if rid.startswith("NFR-")]
    if nfrs and not any(re.search(r"\d", v[1]) for _, v in nfrs):
        rep.warn(spec_path.name, "no NFR contains a number; non-functional requirements need measurable targets (see performance.md)")

    plan_text = read_text(spec_path if track == "lite" else plan_path)
    if "GUIDE.md" not in plan_text:
        rep.fail((spec_path if track == "lite" else plan_path).name,
                 "no handover step: the plan must end with producing docs/GUIDE.md (ovc-explain)")

    if track == "full":
        for rid, (no, body, _) in defs.items():
            if not re.search(r"\bshall\b", body, re.I):
                rep.fail("%s:%d" % (spec_path.name, no), "%s is not in EARS form (the requirement text needs SHALL)" % rid)

    traced = {}
    if track == "lite":
        for t in parse_tables(spec_text):
            c_check = col(t["header"], "check", "test")
            if c_check is None:
                continue
            for no, cells in t["rows"]:
                for rid in REQ_ID_RE.findall(cells[0] if cells else ""):
                    traced[rid] = (no, None, strip_md(cells[c_check]))
        where_name = spec_path.name
    else:
        where_name = plan_path.name
        for t in parse_tables(read_text(plan_path)):
            h = t["header"]
            c_req = col(h, "requirement")
            c_phase = col(h, "phase")
            c_check = col(h, "test", "check")
            if c_req is None or c_phase is None or c_check is None:
                continue
            for no, cells in t["rows"]:
                for rid in REQ_ID_RE.findall(cells[c_req]):
                    traced[rid] = (no, strip_md(cells[c_phase]), strip_md(cells[c_check]))

    for rid in defs:
        if rid not in traced:
            rep.fail(where_name, "requirement %s is missing from the traceability table" % rid)
            continue
        no, phase, check = traced[rid]
        where = "%s:%d" % (where_name, no)
        if phase is not None and is_placeholder(phase):
            rep.fail(where, "%s has no phase" % rid)
        if not EVIDENCE_RE.match(check):
            rep.fail(where, "%s needs a typed check (test: ..., scan: ..., or manual: ...); found %r" % (rid, check))
    for rid in traced:
        if rid not in defs:
            rep.warn(where_name, "traceability lists %s, which is not defined in %s" % (rid, spec_path.name))
    return defs


def check_lite_checklist(sec_path, rep):
    text = read_text(sec_path)
    items = []
    for no, line in lines_outside_fences(text):
        m = re.match(r"^\s*[-*]\s+\[([ xX])\]\s+(.*)$", line)
        if m:
            items.append((no, m.group(1).lower() == "x", m.group(2)))
    if len(items) < 10:
        rep.fail(sec_path.name, "Lite security checklist needs at least 10 checkbox items; found %d" % len(items))
    for no, done, body in items:
        if done and not re.search(r"(verified by\s+(test|scan|manual)\s*:\s*\S|n/a\s*:\s*\S)", body, re.I):
            rep.fail("%s:%d" % (sec_path.name, no),
                     "ticked item needs 'verified by test:/scan:/manual: ...' or 'N/A: <reason>'")


def check_agents(root, docs_dir, rep, level=None, require_guide=True):
    agents = root / "AGENTS.md"
    if not agents.is_file():
        rep.fail("AGENTS.md", "missing at project root")
        return
    text = read_text(agents)
    n_lines = len(text.splitlines())
    if n_lines > 120:
        rep.warn("AGENTS.md", "%d lines; keep it short (include only what the agent cannot infer)" % n_lines)
    dname = docs_dir.name
    if dname + "/DECISIONS.md" not in text:
        rep.fail("AGENTS.md", "must reference %s/DECISIONS.md" % dname)
    if require_guide and "GUIDE.md" not in text:
        rep.fail("AGENTS.md", "Definition of done must include producing %s/GUIDE.md (the handover guide)" % dname)
    for m in re.finditer(r"(?<![\w/.-])(%s/[\w./-]+\.md)" % re.escape(dname), text):
        target = root / m.group(1)
        if target.name == "GUIDE.md":
            continue  # created at the end of the build, not at spec time
        if not target.is_file():
            rep.fail("AGENTS.md", "points to %s, which does not exist" % m.group(1))
    if level == "beginner" and "explain" not in text.lower():
        rep.warn("AGENTS.md", "level is beginner: add the 'Explain as you go' rule (see agents-md.md)")
    if "docs/" in text and dname != "docs":
        rep.warn("AGENTS.md", "mentions docs/ but this project uses %s/" % dname)


def required_files(track, docs_dir):
    d = docs_dir
    common = [d / "SECURITY.md", d / "DECISIONS.md"]
    if track == "lite":
        return [d / "SPEC.md"] + common
    base = [d / "PRD.md", d / "ARCHITECTURE.md", d / "BUILD_PLAN.md"] + common
    return base


def check_greenfield(root, docs_dir, track, rep, allow_oq, level=None):
    for f in required_files(track, docs_dir):
        if not f.is_file():
            rep.fail(str(f.relative_to(root)), "required file for the %s track is missing" % track)
    check_agents(root, docs_dir, rep, level)

    sec = docs_dir / "SECURITY.md"
    if sec.is_file():
        if track == "lite":
            check_lite_checklist(sec, rep)
        else:
            check_status_table(sec, rep, track)

    if track == "lite":
        spec = docs_dir / "SPEC.md"
        if spec.is_file():
            check_trace(spec, None, track, rep)
    else:
        prd, plan = docs_dir / "PRD.md", docs_dir / "BUILD_PLAN.md"
        if prd.is_file() and plan.is_file():
            check_trace(prd, plan, track, rep)

    if track == "full":
        arch = docs_dir / "ARCHITECTURE.md"
        if arch.is_file():
            atext = read_text(arch)
            if not re.search(r"^#+\s.*data[- ]flow", atext, re.I | re.M):
                rep.fail(arch.name, "Full track needs a data-flow diagram section (heading containing 'data-flow')")
            elif "```mermaid" not in atext:
                rep.warn(arch.name, "no mermaid diagram found in the data-flow section")
        adrs = sorted((docs_dir / "adr").glob("ADR-*.md")) if (docs_dir / "adr").is_dir() else []
        if not adrs:
            rep.fail("%s/adr" % docs_dir.name, "Full track needs at least one ADR file (ADR-001-<slug>.md)")

    scan = [root / "AGENTS.md"] + sorted(docs_dir.glob("*.md")) + sorted((docs_dir / "adr").glob("*.md"))
    scan = [f for f in scan if f.name != "project-brief.md"]
    check_open_questions(scan, rep, allow_oq)


def check_brownfield(root, docs_dir, rep, allow_oq):
    check_agents(root, docs_dir, rep, require_guide=False)
    sec = docs_dir / "SECURITY.md"
    if sec.is_file():
        check_status_table(sec, rep, "standard")
    else:
        rep.fail(str(sec.relative_to(root)), "missing")
    gaps = docs_dir / "GAPS.md"
    if not gaps.is_file():
        rep.fail(str(gaps.relative_to(root)), "missing")
    else:
        text = read_text(gaps)
        has_row = any(
            col(t["header"], "gap") is not None and t["rows"] for t in parse_tables(text)
        )
        if not has_row and not re.search(r"no gaps found", text, re.I):
            rep.fail(gaps.name, "needs at least one gap row, or the words 'No gaps found' plus what was checked")
    if not (docs_dir / "DECISIONS.md").is_file():
        rep.fail(str((docs_dir / "DECISIONS.md").relative_to(root)), "missing")
    scan = [root / "AGENTS.md"] + sorted(docs_dir.glob("*.md"))
    check_open_questions(scan, rep, allow_oq)


# ------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="OVC Framework v2 spec checker")
    ap.add_argument("--root", help="project root (contains AGENTS.md)")
    ap.add_argument("--brief", help="path to project-brief.md (header is validated; track is read from it)")
    ap.add_argument("--track", choices=TRACKS, help="override the track (normally read from the brief)")
    ap.add_argument("--docs-dir", default="docs", help="docs folder relative to root (default: docs)")
    ap.add_argument("--mode", choices=("greenfield", "brownfield"), default="greenfield")
    ap.add_argument("--allow-open-questions", action="store_true",
                    help="downgrade leftover open questions to warnings (only after the person chose to leave them)")
    args = ap.parse_args(argv)

    track = args.track
    level = None
    if args.brief:
        code, brief_track, brief_level, msgs = check_brief(args.brief)
        for m in msgs:
            print(m if m.startswith("WARN") else "REJECTED  " + m)
        if code != 0:
            return code
        if not args.root:
            print("Brief OK. Track: %s. Level: %s" % (brief_track, brief_level))
            return 0
        if track and track != brief_track:
            print("REJECTED  --track %s conflicts with the brief's track %s" % (track, brief_track))
            return 2
        track = brief_track
        level = brief_level

    if not args.root:
        ap.error("give --brief and/or --root")

    root = Path(args.root).resolve()
    docs_dir = root / args.docs_dir
    rep = Report()

    if args.mode == "brownfield":
        check_brownfield(root, docs_dir, rep, args.allow_open_questions)
    else:
        if not track:
            track = "lite" if (docs_dir / "SPEC.md").is_file() else "standard"
            print("note: no brief or --track given; inferred track '%s'" % track)
        print("Checking %s project at %s (track: %s)" % (args.mode, root, track))
        check_greenfield(root, docs_dir, track, rep, args.allow_open_questions, level)

    rep.print()
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main())
