#!/usr/bin/env python3
"""OVC Framework guide checker.

Plain Python 3.8+, standard library only.

Checks that docs/GUIDE.md (the Builder's Guide) matches the real project:
paths exist, file:line references are real, every requirement is covered,
test evidence points at tests that exist, measured numbers carry evidence,
and the security section does not hide unverified items.

It checks that the guide is *consistent with the project*. It cannot tell
whether an explanation is correct; a human still has to read it.

Usage:
  python3 check_guide.py --root . [--guide docs/GUIDE.md] [--docs-dir docs]
                         [--level beginner|intermediate|expert]

Exit codes: 0 pass, 1 checks failed, 2 bad usage / guide missing.
"""

import argparse
import re
import sys
from pathlib import Path

LEVELS = ("beginner", "intermediate", "expert")
DEFAULT_LEVEL = {"lite": "beginner", "standard": "intermediate", "full": "intermediate"}
MIN_QUESTIONS = {"beginner": 5, "intermediate": 3, "expert": 0}
STATUSES = {"done": "Done", "partial": "Partial", "not built": "Not built"}
REQUIRED_HEADINGS = [
    "at a glance", "how to run", "big picture", "project tour", "walkthrough",
    "requirements coverage", "security status", "performance",
    "limits and known gaps", "changing it safely", "could not verify",
]
NOT_FOR_EXPERT = ["concepts", "check yourself"]
EVIDENCE_RE = re.compile(r"^(test|scan|manual)\s*:\s*\S", re.I)
TEST_REF_RE = re.compile(r"test:\s*([\w./\\-]+)::([\w.\-]+)", re.I)
REQ_ID_RE = re.compile(r"\b(?:FR|NFR)-\d{3}\b")
REQ_DEF_RE = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+|\|\s*)\**\s*((?:FR|NFR)-\d{3})\b")
LINE_REF_RE = re.compile(r"`([\w./\\-]+\.[A-Za-z0-9]+):(\d+)(?:[-\u2013](\d+))?`")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
TEMPLATE_LEFTOVERS = ["<question>", "<answer", "<Project Name>", "<level>", "<date>", "<what happens"]


class Report:
    def __init__(self):
        self.fails, self.warns = [], []

    def fail(self, where, msg):
        self.fails.append((where, msg))

    def warn(self, where, msg):
        self.warns.append((where, msg))

    def print(self):
        for w, m in self.fails:
            print("FAIL  %s: %s" % (w, m))
        for w, m in self.warns:
            print("WARN  %s: %s" % (w, m))
        if self.fails:
            print("\nRESULT: FAIL (%d failure(s), %d warning(s))" % (len(self.fails), len(self.warns)))
        else:
            print("\nRESULT: PASS (%d warning(s))" % len(self.warns))


# ----------------------------------------------------------------- helpers

def read_text(p):
    return Path(p).read_text(encoding="utf-8-sig")


def strip_md(s):
    return re.sub(r"[*`_]", "", s.replace("\\|", "|")).strip()


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def is_sep(cells):
    return bool(cells) and all(re.match(r"^:?-{2,}:?$", c.strip()) for c in cells)


def parse_tables(lines):
    """lines: list of str. Returns [{'header': [...lower], 'rows': [(idx, cells)]}]; skips fenced code."""
    tables, cur, in_fence, i = [], None, False, 0
    while i < len(lines):
        ln = lines[i]
        if FENCE_RE.match(ln):
            in_fence, cur = not in_fence, None
            i += 1
            continue
        if in_fence or not ln.strip().startswith("|"):
            cur = None
            i += 1
            continue
        if cur is None:
            if i + 1 < len(lines) and is_sep(split_row(lines[i + 1])):
                cur = {"header": [strip_md(h).lower() for h in split_row(ln)], "rows": []}
                tables.append(cur)
                i += 2
                continue
            i += 1
            continue
        cells = split_row(ln)
        n = len(cur["header"])
        cells = (cells + [""] * n) if len(cells) < n else cells
        cur["rows"].append((i, cells))
        i += 1
    return tables


def col(header, *needles):
    for idx, h in enumerate(header):
        if any(n in h for n in needles):
            return idx
    return None


def outside_fences(lines):
    in_fence = False
    for i, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i, ln


def get_sections(lines):
    """Return list of dicts: level, title (lower), start, end (exclusive), body (lines)."""
    heads = []
    for i, ln in outside_fences(lines):
        m = re.match(r"^(#{2,4})\s+(.*)$", ln)
        if m:
            heads.append((i, len(m.group(1)), m.group(2).strip().lower()))
    secs = []
    for idx, (i, lvl, title) in enumerate(heads):
        end = len(lines)
        for j, lvl2, _ in heads[idx + 1:]:
            if lvl2 <= lvl:
                end = j
                break
        secs.append({"level": lvl, "title": title, "start": i, "end": end, "body": lines[i + 1:end]})
    return secs


def find_section(secs, keyword):
    for s in secs:
        if keyword in s["title"]:
            return s
    return None


def front_matter(text):
    ls = text.lstrip("\ufeff").splitlines()
    if not ls or ls[0].strip() != "---":
        return {}
    meta = {}
    for ln in ls[1:]:
        if ln.strip() == "---":
            return meta
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ln)
        if m:
            meta[m.group(1).lower()] = m.group(2).strip().strip("\"'")
    return {}


def detect_level(root, docs_dir, explicit):
    if explicit:
        return explicit, "from --level"
    brief = docs_dir / "project-brief.md"
    if not brief.is_file():
        brief = root / "project-brief.md"
    if brief.is_file():
        meta = front_matter(read_text(brief))
        lvl = meta.get("level", "").lower()
        if lvl in LEVELS:
            return lvl, "from the brief"
        trk = meta.get("track", "").lower()
        if trk in DEFAULT_LEVEL:
            return DEFAULT_LEVEL[trk], "default for track %s" % trk
    return "intermediate", "default (no brief found)"


def path_exists(root, p):
    p = p.strip().strip("`").rstrip("/")
    return bool(p) and (root / p).exists()


def paths_in(text):
    """Pull path-like tokens (optionally with :line) out of a cell."""
    out = []
    for tok in re.findall(r"`([^`]+)`", text) or re.split(r"[,;\s]+", text):
        tok = tok.strip()
        tok = re.sub(r":\d+(?:[-\u2013]\d+)?$", "", tok)
        if tok and ("/" in tok or "." in tok):
            out.append(tok)
    return out


# ------------------------------------------------------------------ checks

def check_headings(secs, level, rep, gname):
    titles = [s["title"] for s in secs if s["level"] == 2]
    needed = list(REQUIRED_HEADINGS)
    if level != "expert":
        needed += NOT_FOR_EXPERT
    for kw in needed:
        if not any(kw in t for t in titles):
            rep.fail(gname, "missing required section containing %r" % kw)


def body_text(sec):
    return "\n".join(l for l in sec["body"] if l.strip())


def check_tour(root, secs, lines, rep, gname):
    sec = find_section(secs, "project tour")
    if not sec:
        return
    tables = parse_tables(sec["body"])
    rows = [(sec["start"] + 1 + i, c) for t in tables if col(t["header"], "path") is not None for i, c in t["rows"]]
    if not rows:
        rep.fail(gname, "Project tour needs a table with a Path column and at least one row")
        return
    for no, cells in rows:
        p = strip_md(cells[0])
        if not p:
            continue
        if not path_exists(root, p):
            rep.fail("%s:%d" % (gname, no + 1), "Project tour lists %r, which does not exist" % p)
        if len(cells) > 1 and not strip_md(cells[1]):
            rep.fail("%s:%d" % (gname, no + 1), "Project tour entry %r has no description" % p)


def check_line_refs(root, lines, rep, gname):
    cache = {}
    for i, ln in outside_fences(lines):
        for m in LINE_REF_RE.finditer(ln):
            rel, a, b = m.group(1), int(m.group(2)), m.group(3)
            f = root / rel
            if not f.is_file():
                rep.fail("%s:%d" % (gname, i + 1), "reference %s:%d points to a file that does not exist" % (rel, a))
                continue
            if rel not in cache:
                cache[rel] = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
            last = int(b) if b else a
            if a < 1 or last > cache[rel] or (b and int(b) < a):
                rep.fail("%s:%d" % (gname, i + 1), "reference %s:%s is outside the file (%d lines)" % (rel, b and "%d-%s" % (a, b) or a, cache[rel]))


def requirement_ids(root, docs_dir):
    for name in ("PRD.md", "SPEC.md"):
        f = docs_dir / name
        if f.is_file():
            ids = []
            for _, ln in outside_fences(read_text(f).splitlines()):
                m = REQ_DEF_RE.match(ln)
                if m and m.group(1) not in ids:
                    ids.append(m.group(1))
            return ids, name
    return [], None


def check_test_refs(root, evidence, rep, where):
    for m in TEST_REF_RE.finditer(evidence):
        rel, name = m.group(1), m.group(2)
        f = root / rel
        if not f.is_file():
            rep.fail(where, "evidence cites test file %s, which does not exist" % rel)
        elif not re.search(r"(?<![\w])%s(?![\w])" % re.escape(name), f.read_text(encoding="utf-8", errors="replace")):
            rep.fail(where, "evidence cites test %r, which is not found in %s" % (name, rel))


def check_coverage(root, docs_dir, secs, rep, gname):
    sec = find_section(secs, "requirements coverage")
    if not sec:
        return
    ids, src = requirement_ids(root, docs_dir)
    tables = [t for t in parse_tables(sec["body"]) if col(t["header"], "status") is not None]
    if not tables:
        rep.fail(gname, "Requirements coverage needs a table with ID, Where it lives, Status, and Evidence columns")
        return
    t = tables[0]
    h = t["header"]
    c_id, c_where, c_status, c_ev = col(h, "id"), col(h, "where"), col(h, "status"), col(h, "evidence")
    if None in (c_id, c_where, c_status, c_ev):
        rep.fail(gname, "Requirements coverage table must have columns: ID, Where it lives, Status, Evidence")
        return
    seen = {}
    for i, cells in t["rows"]:
        where = "%s:%d" % (gname, sec["start"] + 2 + i)
        rid_list = REQ_ID_RE.findall(cells[c_id])
        if not rid_list:
            continue
        status_raw = strip_md(cells[c_status]).lower()
        if status_raw not in STATUSES:
            rep.fail(where, "status %r must be Done, Partial, or Not built" % cells[c_status])
            continue
        status = STATUSES[status_raw]
        ev = strip_md(cells[c_ev])
        for rid in rid_list:
            seen[rid] = status
        if status == "Done":
            if not EVIDENCE_RE.match(ev):
                rep.fail(where, "%s is Done but has no typed evidence (test:, scan:, or manual:)" % ", ".join(rid_list))
        elif not ev:
            rep.fail(where, "%s is %s but the Evidence cell is empty (say what is proven / why not built)" % (", ".join(rid_list), status))
        check_test_refs(root, cells[c_ev], rep, where)
        if status in ("Done", "Partial"):
            ps = paths_in(cells[c_where])
            if not ps:
                rep.fail(where, "%s is %s but 'Where it lives' names no file" % (", ".join(rid_list), status))
            for p in ps:
                if not path_exists(root, p):
                    rep.fail(where, "'Where it lives' names %r, which does not exist" % p)
    if not ids:
        rep.warn(gname, "no PRD.md or SPEC.md with requirement IDs found in %s; coverage not cross-checked" % docs_dir.name)
    for rid in ids:
        if rid not in seen:
            rep.fail(gname, "requirement %s (from %s) is missing from Requirements coverage" % (rid, src))
    for rid in seen:
        if ids and rid not in ids:
            rep.warn(gname, "coverage lists %s, which is not defined in %s" % (rid, src))


def check_performance(secs, rep, gname):
    sec = find_section(secs, "performance")
    if not sec:
        return
    tables = [t for t in parse_tables(sec["body"]) if col(t["header"], "measured") is not None]
    if not tables:
        rep.fail(gname, "Performance needs a table with Target, Goal, Measured, and How measured columns")
        return
    t = tables[0]
    h = t["header"]
    c_m, c_how = col(h, "measured"), col(h, "how")
    if c_how is None:
        rep.fail(gname, "Performance table needs a 'How measured' column")
        return
    if not t["rows"]:
        rep.fail(gname, "Performance table has no rows (use 'Not measured' where nothing was measured)")
    for i, cells in t["rows"]:
        where = "%s:%d" % (gname, sec["start"] + 2 + i)
        m = strip_md(cells[c_m])
        if not m:
            rep.fail(where, "Measured cell is empty (write a measured value or exactly 'Not measured')")
        elif m.lower() != "not measured":
            if not re.search(r"\d", m):
                rep.fail(where, "Measured value %r has no number; write 'Not measured' if nothing was measured" % m)
            if not EVIDENCE_RE.match(strip_md(cells[c_how])):
                rep.fail(where, "a measured number needs a typed 'How measured' (test:, scan:, or manual:)")


def unverified_security_items(docs_dir):
    f = docs_dir / "SECURITY.md"
    if not f.is_file():
        return 0
    lines = read_text(f).splitlines()
    n = sum(1 for _, ln in outside_fences(lines) if re.match(r"^\s*[-*]\s+\[ \]\s", ln))
    for t in parse_tables(lines):
        c = col(t["header"], "status")
        if c is not None and col(t["header"], "verified") is not None:
            for _, cells in t["rows"]:
                if strip_md(cells[c]).lower() in ("planned", "open"):
                    n += 1
    return n


def check_security(docs_dir, secs, rep, gname):
    sec = find_section(secs, "security status")
    if not sec:
        return
    txt = body_text(sec)
    if len(txt) < 20:
        rep.fail(gname, "Security status is empty")
        return
    n = unverified_security_items(docs_dir)
    if n and not re.search(r"\b(open|planned|unverified|not yet|not verified|remaining|not done)\b", txt, re.I):
        rep.fail(gname, "SECURITY.md still has %d unverified item(s) but the guide's Security status does not mention any open, planned, or unverified work" % n)
    elif n:
        rep.warn(gname, "SECURITY.md has %d unverified item(s); make sure the guide lists each one" % n)


def check_questions(secs, level, rep, gname):
    sec = find_section(secs, "check yourself")
    need = MIN_QUESTIONS[level]
    if not sec:
        return
    q = {}
    a = {}
    for ln in sec["body"]:
        m = re.match(r"^\s*\**Q(\d+)\**[.)]\s*(\S.*)$", ln)
        if m:
            q[int(m.group(1))] = m.group(2)
        m = re.match(r"^\s*\**A(\d+)\**[.)]\s*(\S.*)$", ln)
        if m:
            a[int(m.group(1))] = m.group(2)
    if len(q) < need:
        rep.fail(gname, "Check yourself has %d question(s); %s level needs at least %d" % (len(q), level, need))
    for n in sorted(q):
        if n not in a:
            rep.fail(gname, "question Q%d has no answer A%d" % (n, n))


def check_unverified_section(secs, rep, gname):
    sec = find_section(secs, "could not verify")
    if sec and len(body_text(sec)) < 3:
        rep.fail(gname, "'What I could not verify' is empty (write what was not checked, or 'Nothing' if true)")


def check_placeholders(lines, rep, gname):
    for i, ln in outside_fences(lines):
        if re.search(r"\[OPEN QUESTION\b", re.sub(r"`[^`]*`", "", ln), re.I):
            rep.fail("%s:%d" % (gname, i + 1), "unresolved open-question marker")
        for tok in TEMPLATE_LEFTOVERS:
            if tok in ln:
                rep.fail("%s:%d" % (gname, i + 1), "leftover template placeholder %r" % tok)
                break
        if re.search(r"\b(TODO|TBD|FIXME)\b", ln):
            rep.warn("%s:%d" % (gname, i + 1), "placeholder word in the guide: %s" % ln.strip()[:80])


# -------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="OVC Builder's Guide checker")
    ap.add_argument("--root", required=True, help="project root")
    ap.add_argument("--guide", help="guide path relative to root (default: <docs-dir>/GUIDE.md)")
    ap.add_argument("--docs-dir", default="docs")
    ap.add_argument("--level", choices=LEVELS)
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    docs_dir = root / args.docs_dir
    gpath = root / args.guide if args.guide else docs_dir / "GUIDE.md"
    if not gpath.is_file():
        print("REJECTED  guide not found: %s" % gpath)
        return 2
    text = read_text(gpath)
    lines = text.splitlines()
    gname = gpath.name
    level, why = detect_level(root, docs_dir, args.level)
    print("Checking %s (level: %s, %s)" % (gpath, level, why))

    rep = Report()
    secs = get_sections(lines)
    check_headings(secs, level, rep, gname)
    check_tour(root, secs, lines, rep, gname)
    check_line_refs(root, lines, rep, gname)
    check_coverage(root, docs_dir, secs, rep, gname)
    check_performance(secs, rep, gname)
    check_security(docs_dir, secs, rep, gname)
    check_questions(secs, level, rep, gname)
    check_unverified_section(secs, rep, gname)
    check_placeholders(lines, rep, gname)
    rep.print()
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main())
