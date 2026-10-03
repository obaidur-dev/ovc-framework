#!/usr/bin/env python3
"""Tests for the OVC v2 framework. Standard library only.

Run from the repository root:
    python3 -m unittest discover -s evals -v

Covers: scripts/check_specs.py behaviour (using the worked examples, mutated),
and structural lint of both skills (limits, tool neutrality, shared template).
"""

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "ovc-specify" / "scripts" / "check_specs.py"
LITE = REPO / "examples" / "lite-study-timer"
FULL = REPO / "examples" / "full-lab-booking"
DISCOVER = REPO / "ovc-discover"
SPECIFY = REPO / "ovc-specify"
EXPLAIN = REPO / "ovc-explain"
SKILLS = (DISCOVER, SPECIFY, EXPLAIN)
GUIDE_SCRIPT = EXPLAIN / "scripts" / "check_guide.py"


def run(*args):
    p = subprocess.run([sys.executable, str(SCRIPT)] + [str(a) for a in args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def run_guide(*args):
    p = subprocess.run([sys.executable, str(GUIDE_SCRIPT)] + [str(a) for a in args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class Sandbox:
    """Copy of an example project that tests can mutate."""

    def __init__(self, src):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "proj"
        shutil.copytree(src, self.root)

    def path(self, rel):
        return self.root / rel

    def edit(self, rel, fn):
        p = self.path(rel)
        p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")

    def check(self, *extra):
        return run("--root", self.root, "--brief", self.root / "docs" / "project-brief.md", *extra)

    def cleanup(self):
        self.tmp.cleanup()


class SandboxCase(unittest.TestCase):
    SRC = LITE

    def setUp(self):
        self.sb = Sandbox(self.SRC)
        self.addCleanup(self.sb.cleanup)


# ----------------------------------------------------------------- brief

class BriefHeader(unittest.TestCase):
    def write(self, text):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        p = Path(d.name) / "project-brief.md"
        p.write_text(text, encoding="utf-8")
        return p

    def test_valid_brief(self):
        code, out = run("--brief", LITE / "docs" / "project-brief.md")
        self.assertEqual(code, 0, out)
        self.assertIn("Track: lite", out)

    def test_unknown_version_rejected_with_clear_message(self):
        p = self.write("---\novc-brief-version: 3\ntrack: lite\nproject: X\n---\n# Brief\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 2)
        self.assertIn("Unsupported ovc-brief-version", out)

    def test_v1_brief_without_header_rejected_with_upgrade_hint(self):
        p = self.write("# Project Brief: Old\n\n## Problem\nx\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 2)
        self.assertIn("v1", out)

    def test_header_without_version_rejected(self):
        p = self.write("---\ntrack: lite\nproject: X\n---\n# Brief\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 2)

    def test_invalid_track_rejected(self):
        p = self.write("---\novc-brief-version: 2\ntrack: huge\nproject: X\n---\n# Brief\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 2)
        self.assertIn("track", out)

    def test_level_is_reported_and_defaults_by_track(self):
        code, out = run("--brief", LITE / "docs" / "project-brief.md")
        self.assertIn("Level: beginner", out)
        p = self.write("---\novc-brief-version: 2\ntrack: standard\nproject: X\n---\n# Brief\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 0, out)
        self.assertIn("Level: intermediate", out)

    def test_invalid_level_rejected(self):
        p = self.write("---\novc-brief-version: 2\ntrack: lite\nlevel: wizard\nproject: X\n---\n# Brief\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 2)
        self.assertIn("level", out)

    def test_old_brief_without_level_still_valid(self):
        p = self.write("---\novc-brief-version: 2\ntrack: full\nproject: X\n---\n# Brief\n")
        code, out = run("--brief", p)
        self.assertEqual(code, 0, out)

    def test_missing_file(self):
        code, _ = run("--brief", "/nonexistent/brief.md")
        self.assertEqual(code, 2)


# ------------------------------------------------------------------ lite

class LiteTrack(SandboxCase):
    SRC = LITE

    def test_example_passes(self):
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)

    def test_leftover_open_question_fails(self):
        self.sb.edit("docs/SPEC.md", lambda t: t.replace("## Open questions\nNone.",
                                                          "## Open questions\n[OPEN QUESTION: which hosting?]"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("unresolved open question", out)

    def test_open_question_allowed_with_flag(self):
        self.sb.edit("docs/SPEC.md", lambda t: t.replace("## Open questions\nNone.",
                                                          "## Open questions\n[OPEN QUESTION: which hosting?]"))
        code, out = self.sb.check("--allow-open-questions")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN", out)

    def test_open_question_text_in_inline_code_is_ignored(self):
        self.sb.edit("docs/SPEC.md", lambda t: t + "\nThe marker looks like `[OPEN QUESTION: x]` in prose.\n")
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)

    def test_requirement_without_typed_check_fails(self):
        self.sb.edit("docs/SPEC.md", lambda t: t.replace(
            "test: tests/timer.test.js::counts_down_from_25_minutes, then manual: press Start and Pause in a browser", "works"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("FR-001", out)

    def test_ticked_item_without_evidence_fails(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace("- [ ] 8. ", "- [x] 8. "))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("ticked item needs", out)

    def test_ticked_item_with_evidence_passes(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace(
            "- [ ] 8. Anything reachable beyond your own laptop uses HTTPS. (Not done: the app is not published yet. Tick after deploying to GitHub Pages and confirming the padlock.)",
            "- [x] 8. Anything reachable beyond your own laptop uses HTTPS. - verified by manual: opened the published page and saw the padlock"))
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)

    def test_short_checklist_fails(self):
        self.sb.edit("docs/SECURITY.md", lambda t: re.sub(r"^- \[[ x]\] 10\..*$", "", t, flags=re.M))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("at least 10", out)

    def test_agents_must_reference_decisions(self):
        self.sb.edit("AGENTS.md", lambda t: t.replace("docs/DECISIONS.md", "docs/SPEC.md"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("DECISIONS", out)

    def test_agents_broken_pointer_fails(self):
        self.sb.edit("AGENTS.md", lambda t: t + "\nSee `docs/NOPE.md`.\n")
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("NOPE", out)

    def test_missing_required_file_fails(self):
        self.sb.path("docs/DECISIONS.md").unlink()
        code, out = self.sb.check()
        self.assertEqual(code, 1)

    def test_plan_without_handover_step_fails(self):
        self.sb.edit("docs/SPEC.md", lambda t: t.replace("GUIDE.md", "the guide"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("handover", out)

    def test_agents_without_guide_in_definition_of_done_fails(self):
        self.sb.edit("AGENTS.md", lambda t: t.replace("`docs/GUIDE.md`", "the guide").replace("GUIDE.md", "the guide"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("GUIDE.md", out)

    def test_guide_file_need_not_exist_at_spec_time(self):
        self.sb.path("docs/GUIDE.md").unlink()
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)

    def test_beginner_without_explain_rule_warns(self):
        self.sb.edit("AGENTS.md", lambda t: t.replace("Explain as you go", "Be concise").replace("explanation", "note").replace("explain", "note"))
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)
        self.assertIn("Explain as you go", out)

    def test_nfr_without_numbers_warns(self):
        self.sb.edit("docs/SPEC.md", lambda t: t.replace("25 minutes", "a while").replace("1 second", "a moment").replace("50 KB", "a small size"))
        code, out = self.sb.check()
        self.assertIn("measurable", out)


# ------------------------------------------------------------------ full

class FullTrack(SandboxCase):
    SRC = FULL

    def test_example_passes(self):
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)

    def test_requirement_missing_from_build_plan_fails(self):
        self.sb.edit("docs/BUILD_PLAN.md", lambda t: re.sub(r"^\| FR-004 .*$", "", t, flags=re.M))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("FR-004", out)
        self.assertIn("missing from the traceability table", out)

    def test_requirement_without_phase_fails(self):
        self.sb.edit("docs/BUILD_PLAN.md", lambda t: t.replace("| FR-003 | Phase 1 |", "| FR-003 | TBD |"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("no phase", out)

    def test_stride_row_without_status_fails(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace("| Planned | test: tests/test_auth.py::test_lockout_after_five_failures |",
                                                              "|  | test: tests/test_auth.py::test_lockout_after_five_failures |"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("no status", out)

    def test_unknown_status_fails(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace("| Open | |", "| Fixed | |"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("unknown status", out)

    def test_mitigated_without_evidence_fails(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace(
            "| Mitigated | test: tests/test_authz.py::test_student_cannot_decide |", "| Mitigated | done |"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("Mitigated", out)

    def test_mitigated_with_blank_evidence_fails(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace(
            "| Mitigated | test: tests/test_authz.py::test_booking_read_is_owner_only |", "| Mitigated |  |"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)

    def test_all_four_statuses_present_in_example(self):
        text = (FULL / "docs" / "SECURITY.md").read_text()
        for s in ("Planned", "Mitigated", "Accepted risk", "Open"):
            self.assertRegex(text, r"\|\s*%s\s*\|" % s)

    def test_requirement_without_shall_fails_on_full(self):
        self.sb.edit("docs/PRD.md", lambda t: t.replace("THE system SHALL show a booking only", "The system shows a booking only"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("EARS", out)

    def test_missing_adr_fails_on_full(self):
        shutil.rmtree(self.sb.path("docs/adr"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)
        self.assertIn("ADR", out)

    def test_missing_data_flow_fails_on_full(self):
        self.sb.edit("docs/ARCHITECTURE.md", lambda t: t.replace("## Data-flow diagram", "## Overview of flow"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)

    def test_planned_without_check_fails_on_full(self):
        self.sb.edit("docs/SECURITY.md", lambda t: t.replace(
            "| Planned | manual: inspect cookie flags in browser dev tools after Phase 2 |", "| Planned |  |"))
        code, out = self.sb.check()
        self.assertEqual(code, 1)

    def test_track_conflict_rejected(self):
        code, out = self.sb.check("--track", "lite")
        self.assertEqual(code, 2)


class StandardTrackDerivedFromFull(SandboxCase):
    """Standard does not require EARS, ADRs, or a diagram."""
    SRC = FULL

    def test_standard_relaxes_full_only_rules(self):
        self.sb.edit("docs/project-brief.md", lambda t: t.replace("track: full", "track: standard"))
        shutil.rmtree(self.sb.path("docs/adr"))
        self.sb.edit("docs/PRD.md", lambda t: t.replace("THE system SHALL show a booking only", "The system shows a booking only"))
        self.sb.edit("docs/ARCHITECTURE.md", lambda t: t.replace("## Data-flow diagram", "## Flow"))
        code, out = self.sb.check()
        self.assertEqual(code, 0, out)


# -------------------------------------------------------------- brownfield

class Brownfield(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "AGENTS.md").write_text(
            "# AGENTS.md\n\nSee `docs/SECURITY.md`, `docs/GAPS.md`, `docs/DECISIONS.md`.\n", encoding="utf-8")
        (self.root / "docs" / "SECURITY.md").write_text(
            "# Security\n\n| ID | Component | Category | Threat | Mitigation | Status | Verified by |\n"
            "|---|---|---|---|---|---|---|\n"
            "| T-001 | Login | Spoofing | Weak hashing | argon2 | Mitigated | manual: reviewed src/auth.py lines 40-80 |\n"
            "| T-002 | Upload | Tampering | Executable upload | none found | Open | |\n", encoding="utf-8")
        (self.root / "docs" / "GAPS.md").write_text(
            "# Gaps\n\n| ID | Area | Gap | Evidence | Risk | Suggested fix |\n|---|---|---|---|---|---|\n"
            "| G-001 | Secrets | .env tracked | manual: git ls-files | High | rotate keys |\n", encoding="utf-8")
        (self.root / "docs" / "DECISIONS.md").write_text("# Decision log\n", encoding="utf-8")

    def check(self, *extra):
        return run("--root", self.root, "--mode", "brownfield", *extra)

    def test_valid_brownfield_passes(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_missing_gaps_fails(self):
        (self.root / "docs" / "GAPS.md").unlink()
        code, _ = self.check()
        self.assertEqual(code, 1)

    def test_mitigated_without_evidence_fails(self):
        p = self.root / "docs" / "SECURITY.md"
        p.write_text(p.read_text().replace("manual: reviewed src/auth.py lines 40-80", "looks fine"))
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_no_gaps_found_statement_accepted(self):
        (self.root / "docs" / "GAPS.md").write_text("# Gaps\n\nNo gaps found. Checked: auth, deps, secrets.\n")
        code, out = self.check()
        self.assertEqual(code, 0, out)


# ----------------------------------------------------------- skill lint

def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "no frontmatter in %s" % path
    fm = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_-]+:", line):
            key, _, val = line.partition(":")
            fm[key] = val.strip()
        elif key and line.startswith(" "):
            fm[key] += " " + line.strip()
    return fm, text[m.end():]


class SkillLint(unittest.TestCase):
    def test_limits_and_names(self):
        for d in SKILLS:
            fm, body = frontmatter(d / "SKILL.md")
            self.assertEqual(fm["name"], d.name)
            self.assertRegex(fm["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
            self.assertLessEqual(len(fm["name"]), 64)
            self.assertLessEqual(len(fm["description"]), 1024, d.name)
            self.assertGreater(len(fm["description"]), 100)
            total = len((d / "SKILL.md").read_text().splitlines())
            self.assertLess(total, 500, "%s SKILL.md has %d lines" % (d.name, total))

    def test_frontmatter_is_valid_yaml_plain_scalar(self):
        """A plain YAML scalar cannot contain ': ' or ' #'. Strict parsers reject it."""
        for d in SKILLS:
            desc = frontmatter(d / "SKILL.md")[0]["description"]
            self.assertNotIn(": ", desc, d.name)
            self.assertNotIn(" #", desc, d.name)
            self.assertFalse(desc[0] in "\"'[{&*!|>%@`", d.name)

    def test_description_has_what_and_when_and_negative_trigger(self):
        for d in SKILLS:
            desc = frontmatter(d / "SKILL.md")[0]["description"]
            self.assertIn("Use when", desc)
            self.assertIn("Do NOT use", desc)

    def test_references_one_level_deep(self):
        for d in SKILLS:
            ref = d / "references"
            for p in ref.rglob("*"):
                if p.is_dir():
                    self.fail("nested directory in references: %s" % p)

    def test_every_reference_is_linked_from_skill_md(self):
        for d in SKILLS:
            body = (d / "SKILL.md").read_text()
            for p in (d / "references").glob("*.md"):
                self.assertIn(p.name, body, "%s not mentioned in %s SKILL.md" % (p.name, d.name))

    def test_expected_reference_files(self):
        self.assertEqual({p.name for p in (DISCOVER / "references").glob("*")},
                         {"brief-template.md", "stack-guide.md", "concept-cards.md"})
        self.assertEqual({p.name for p in (EXPLAIN / "references").glob("*")},
                         {"guide-template.md", "teaching-levels.md"})
        expected = {"brief-template.md", "spec-lite.md", "security-lite.md", "prd.md", "ears.md",
                    "architecture.md", "security.md", "data-model.md", "api-spec.md", "build-plan.md",
                    "agents-md.md", "decisions.md", "brownfield.md", "tool-compat.md",
                    "performance.md", "ai-reliability.md"}
        self.assertEqual({p.name for p in (SPECIFY / "references").glob("*")}, expected)

    def test_brief_template_identical_in_both_skills(self):
        a = (DISCOVER / "references" / "brief-template.md").read_bytes()
        b = (SPECIFY / "references" / "brief-template.md").read_bytes()
        self.assertEqual(a, b)

    def test_no_vendor_names_outside_tool_compat(self):
        pat = re.compile(r"claude|anthropic|codex|cursor|copilot|gemini|opencode|openai", re.I)
        for d in SKILLS:
            for p in list(d.rglob("*.md")) + list(d.rglob("*.py")):
                if p.name == "tool-compat.md":
                    continue
                hits = [m.group(0) for m in pat.finditer(p.read_text())]
                self.assertEqual(hits, [], "%s mentions %s" % (p.relative_to(REPO), hits))

    def test_no_hardcoded_as_of_dates_in_skill_md(self):
        for d in SKILLS:
            text = (d / "SKILL.md").read_text()
            self.assertNotRegex(text, r"(?i)as of (early|late|mid)?\s*(20\d\d|january|february|march|april|may|june|july|august|september|october|november|december)")
            self.assertNotRegex(text, r"20\d\d-\d\d-\d\d")

    def test_tool_compat_has_last_verified(self):
        self.assertRegex((SPECIFY / "references" / "tool-compat.md").read_text(), r"last verified: \d{4}-\d{2}-\d{2}")

    def test_every_skill_has_the_same_version(self):
        versions = set()
        for d in SKILLS:
            m = re.search(r'version: "([\d.]+)"', (d / "SKILL.md").read_text())
            self.assertTrue(m, d.name)
            versions.add(m.group(1))
        self.assertEqual(len(versions), 1, versions)
        self.assertIn("Version %s" % versions.pop(), (REPO / "README.md").read_text())

    def test_templates_do_not_contain_live_open_question_markers(self):
        for p in list((SPECIFY / "references").glob("*.md")) + list((EXPLAIN / "references").glob("*.md")):
            for line in p.read_text().splitlines():
                stripped = re.sub(r"`[^`]*`", "", line)
                self.assertNotRegex(stripped, r"\[OPEN QUESTION", "%s: %s" % (p.name, line))


# ------------------------------------------------- research-claim wording

class ResearchClaims(unittest.TestCase):
    """A statistic without its scope is how a true number becomes a false one."""

    def texts(self):
        skip = {"CHANGELOG.md", "EVIDENCE.md"}
        for p in list(REPO.rglob("*.md")) + list(REPO.rglob("*.json")):
            if p.name in skip or "node_modules" in p.parts or "evals" in p.parts and p.suffix == ".py":
                continue
            yield p, p.read_text(encoding="utf-8")

    def test_quiz_gap_is_in_percentage_points(self):
        for p, t in self.texts():
            if re.search(r"17% lower|about 17%|17 per cent", t):
                self.fail("%s uses the ambiguous '17%%' wording; say 17 percentage points" % p.relative_to(REPO))
            if "2601.20245" in t and "17" in t:
                self.assertIn("percentage point", t, p.relative_to(REPO))

    def test_94_percent_always_carries_its_scope(self):
        for p, t in self.texts():
            if "94%" in t:
                self.assertIn("open-weight", t, "%s: 94%% needs 'open-weight' scope" % p.relative_to(REPO))
                self.assertRegex(t, r"TypeScript", p.relative_to(REPO))

    def test_efficiency_figure_names_the_model(self):
        for p, t in self.texts():
            if re.search(r"3\.12", t):
                self.assertIn("GPT-4", t, "%s: 3.12x is a GPT-4 figure" % p.relative_to(REPO))

    def test_package_hallucination_percentages_keep_both_groups_and_at_least(self):
        for p, t in self.texts():
            if "21.7%" in t:
                self.assertIn("5.2%", t, p.relative_to(REPO))
                self.assertRegex(t, r"(?i)at least", p.relative_to(REPO))
                self.assertRegex(t, r"(?i)open-source", p.relative_to(REPO))

    def test_unverifiable_claims_stay_removed(self):
        banned = ["newer models have narrowed", "newer models have much closer", "McEval", "PROBE"]
        for p, t in self.texts():
            if p.name == "EVIDENCE.md":
                continue
            for b in banned:
                self.assertNotIn(b, t, "%s still contains the removed claim %r" % (p.relative_to(REPO), b))

    def test_44_percent_is_labelled_as_derived(self):
        for p, t in self.texts():
            if re.search(r"\b44%", t):
                self.assertRegex(t, r"(?i)arithmetic|derived", "%s: 44%% must be labelled derived" % p.relative_to(REPO))

    def test_energy_ratios_are_paired_with_the_critique(self):
        for p, t in self.texts():
            if "75.88" in t or "71.90" in t:
                self.assertIn("2410.05460", t, "%s: Pereira ratios need the critique" % p.relative_to(REPO))

    def test_evidence_register_exists_and_is_linked(self):
        self.assertTrue((REPO / "EVIDENCE.md").is_file())
        self.assertIn("EVIDENCE.md", (REPO / "README.md").read_text())


# ----------------------------------------------------------- guide checker

class GuideChecker(unittest.TestCase):
    def setUp(self):
        self.sb = Sandbox(LITE)
        self.addCleanup(self.sb.cleanup)

    def check(self, *extra):
        return run_guide("--root", self.sb.root, *extra)

    def edit_guide(self, fn):
        self.sb.edit("docs/GUIDE.md", fn)

    def test_example_guide_passes(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_missing_guide_is_rejected(self):
        self.sb.path("docs/GUIDE.md").unlink()
        code, out = self.check()
        self.assertEqual(code, 2)

    def test_tour_path_that_does_not_exist_fails(self):
        self.edit_guide(lambda t: t.replace("| `src/store.js` | Saves", "| `src/nope.js` | Saves"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("nope.js", out)

    def test_line_reference_past_end_of_file_fails(self):
        self.edit_guide(lambda t: t.replace("`src/timer.js:45`", "`src/timer.js:999`", 1))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("outside the file", out)

    def test_line_reference_to_missing_file_fails(self):
        self.edit_guide(lambda t: t + "\nSee `src/ghost.js:3`.\n")
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_requirement_missing_from_coverage_fails(self):
        self.edit_guide(lambda t: re.sub(r"^\| FR-003 .*$", "", t, flags=re.M))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("FR-003", out)

    def test_done_without_typed_evidence_fails(self):
        self.edit_guide(lambda t: t.replace("| Done | test: tests/timer.test.js::switches_phase_at_zero |", "| Done | works |"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("typed evidence", out)

    def test_cited_test_that_does_not_exist_fails(self):
        self.edit_guide(lambda t: t.replace("::switches_phase_at_zero", "::does_not_exist"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("does_not_exist", out)

    def test_cited_test_file_that_does_not_exist_fails(self):
        self.edit_guide(lambda t: t.replace("tests/timer.test.js::switches_phase_at_zero", "tests/ghost.test.js::switches_phase_at_zero"))
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_invalid_status_fails(self):
        self.edit_guide(lambda t: t.replace("| Done | test: tests/timer.test.js::switches", "| Finished | test: tests/timer.test.js::switches"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("Done, Partial, or Not built", out)

    def test_partial_with_empty_evidence_fails(self):
        self.edit_guide(lambda t: re.sub(r"(\| FR-003 \|[^|]*\| Partial \|)[^|]*\|", r"\1  |", t))
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_measured_number_without_evidence_fails(self):
        self.edit_guide(lambda t: t.replace("| Load time on a phone | no target set | Not measured | n/a |",
                                            "| Load time on a phone | no target set | 1.2 s | n/a |"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("typed", out)

    def test_measured_without_a_number_fails(self):
        self.edit_guide(lambda t: t.replace("| Load time on a phone | no target set | Not measured | n/a |",
                                            "| Load time on a phone | no target set | fast | scan: looked at it |"))
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_security_section_hiding_open_items_fails(self):
        self.edit_guide(lambda t: re.sub(r"## Security status\n.*?(?=## Performance)",
                                         "## Security status\nEverything is checked and fine, all good here.\n\n", t, flags=re.S))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("unverified", out)

    def test_too_few_questions_for_beginner_fails(self):
        def cut(t):
            for n in (4, 5, 6):
                t = re.sub(r"^Q%d\..*$" % n, "", t, flags=re.M)
                t = re.sub(r"^A%d\..*$" % n, "", t, flags=re.M)
            return t
        self.edit_guide(cut)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("at least 5", out)

    def test_question_without_answer_fails(self):
        self.edit_guide(lambda t: re.sub(r"^A3\..*$", "", t, flags=re.M))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("Q3", out)

    def test_missing_required_section_fails(self):
        self.edit_guide(lambda t: t.replace("## Limits and known gaps", "## Misc"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("limits and known gaps", out)

    def test_empty_could_not_verify_fails(self):
        self.edit_guide(lambda t: re.sub(r"(## What I could not verify\n).*", r"\1", t, flags=re.S))
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_leftover_template_placeholder_fails(self):
        self.edit_guide(lambda t: t + "\nQ9. <question>\n")
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_expert_level_does_not_need_concepts_or_questions(self):
        def strip(t):
            t = re.sub(r"## Concepts\n.*?(?=## Limits)", "", t, flags=re.S)
            t = re.sub(r"## Check yourself\n.*?(?=## What I could not verify)", "", t, flags=re.S)
            return t
        self.edit_guide(strip)
        code, out = self.check("--level", "expert")
        self.assertEqual(code, 0, out)
        code, out = self.check("--level", "beginner")
        self.assertEqual(code, 1)

    def test_unknown_requirement_id_only_warns(self):
        self.edit_guide(lambda t: t.replace("| NFR-003 |", "| NFR-099 | `index.html` | Not built | not planned |\n| NFR-003 |", 1))
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("NFR-099", out)


class RealExampleApp(unittest.TestCase):
    """The Lite example is a real app. Its own tests must pass if Node is installed."""

    def test_example_unit_tests_pass(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed")
        p = subprocess.run([node, "--test"], cwd=LITE, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-800:] + p.stderr[-400:])


if __name__ == "__main__":
    unittest.main()
