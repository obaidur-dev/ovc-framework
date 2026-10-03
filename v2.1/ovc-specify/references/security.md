# SECURITY.md template (Standard and Full tracks)

Load this when writing `docs/SECURITY.md`. On Lite use `security-lite.md`.
Never optional, whatever the project size. Write it after ARCHITECTURE.md (its
trust boundaries are your input) and after DATA_MODEL.md if present.

Sources last verified: 2026-10-02 (Veracode, Spracklen et al. read directly; the
OWASP 2026 edition list was only partly confirmed). If you can search the web,
re-check the figures in "Why this document exists" and use the newest edition;
if you cannot, cite them exactly as written here with the source name and year.

## Why this document exists

AI-assisted code ships security defects that go unnoticed because nobody
stopped to look. This document forces that pause, and the **Verified by**
column forces proof instead of hope.

Evidence to cite (benchmarks of controlled tasks, not predictions for any one
project; say so, and quote the scope with the number):

- Veracode, *2025 GenAI Code Security Report* (30 July 2025): 80 curated coding
  tasks, each offering a secure and an insecure way to complete the code, run on
  100+ LLMs. In 45% of cases the model chose the insecure way, introducing a
  vulnerability in the OWASP Top 10 class. Java had the highest failure rate
  (over 70%); the model failed to defend against cross-site scripting in 86% of
  relevant cases.
- Veracode, *2026 GenAI Code Security Report* (summer 2026): across 100+ models
  tested over four years the average security pass rate is 56% and "hasn't
  moved"; 11 new models were tested across 80 tasks, and the best scored
  68%. (The complementary figure of about 44% failing is simple arithmetic from
  the 56% pass rate, not a number Veracode states.)
- Spracklen et al., *We Have a Package for You!* (arXiv 2406.10279, USENIX
  Security 2025): 16 models, 576,000 generated Python and JavaScript samples; the
  average share of hallucinated packages was **at least** 5.2% for commercial
  models and 21.7% for open-source models, with 205,474 unique invented names.
  Attackers can register those names ("slopsquatting").
- OWASP Top 10 for LLM Applications (2026 edition published August 2026;
  earlier 2025 edition). Category numbers and some names changed between
  editions (for example "System Prompt Leakage" became "Hidden Context
  Exposure"), so **refer to risks by name, not number**, and cite the edition.

## Status key (all four are valid; nothing else is)

| Status | Meaning | Needs |
|---|---|---|
| `Planned` | Mitigation designed, not built | The planned check in "Verified by" |
| `Mitigated` | Built **and** verified | Evidence in "Verified by" (see below) |
| `Accepted risk` | Consciously not fixing | A one-line reason and who accepted it, in "Mitigation" |
| `Open` | Not yet decided or addressed | Nothing; this is honest, blank is not |

**A row cannot be `Mitigated` without evidence.** Evidence is typed:
`test: <test name or path>`, `scan: <tool and result>`, or
`manual: <what was done and what was seen>`. "Done" and "implemented" are not
evidence. Never leave Status empty; an unstated status looks identical to
"never considered".

## Template

```markdown
# Security: <Project Name>

## Data classification
What data the system touches and how sensitive each category is (PII,
credentials, payment data, health data, or "nothing sensitive: <why>").

## Rules and policies that apply
The answer to the compliance question (see below), or an open-question marker
if the person was not sure. Never assume.

## Trust boundaries
Pulled from ARCHITECTURE.md's data flow: [TB-1], [TB-2], ...

## STRIDE threat walkthrough
For each trust boundary or major component, walk the six STRIDE categories and
keep only those that apply. STRIDE is a checklist of six ways software gets
attacked: Spoofing (pretending to be someone), Tampering (changing data),
Repudiation (denying an action with no log to prove it), Information
disclosure (leaking data), Denial of service (making it unavailable), and
Elevation of privilege (gaining rights you should not have).

| ID | Component / boundary | Category | Threat | Mitigation | Status | Verified by |
|---|---|---|---|---|---|---|
| T-001 | Login endpoint [TB-1] | Spoofing | Credential stuffing | Rate limiting, lockout, hashed passwords | Planned | test: tests/test_auth.py::test_lockout |
| T-002 | Admin API [TB-2] | Elevation of privilege | Regular user reaches admin routes | Role check on every route, deny by default | Mitigated | test: tests/test_authz.py::test_admin_routes_forbidden |
| T-003 | Booking export | Information disclosure | Another user's data in export | Filter by owner on the server | Accepted risk | n/a (accepted by project owner: export is admin-only in v1) |

## Auth and authorization approach
How users and services prove who they are, and how access is decided after.

## Secrets and configuration
Where credentials, keys, and config live, how they rotate, and what must
never be committed.

## Dependency check
See the procedure below. Keep a table of packages added:

| Package | Purpose | Exists and spelled right | Maintained | Verified by |
|---|---|---|---|---|

## Logging and audit
What is logged (and what must never be: passwords, tokens, full card numbers).
```

## Dependency check (supply chain)

AI tools sometimes suggest packages that do not exist, and the research above
shows attackers register those names. **Checking that the name exists is not
enough.** Before installing any dependency:

1. Take the name from the package's official documentation or registry page,
   not from AI output or memory.
2. Look it up on the registry (npm, PyPI, crates.io, ...). Note when it was
   first published, release history, maintainers, and download scale.
3. Confirm the linked source repository exists, matches the package, and shows
   recent activity.
4. Compare the name against well-known packages. One character off is a red
   flag; stop and ask the person.
5. Pin the version, commit the lockfile, and run the ecosystem's audit tool
   (for example `npm audit` or `pip-audit`).
6. Record the package in the table above and log it in `docs/DECISIONS.md`.

Tell the AI coding agent in `AGENTS.md` not to add dependencies without this
check.

## If the project itself calls an AI model

Add rows (IDs continuing the table) for at least these OWASP Top 10 for LLM
Applications risks, by name:

| Risk (by name) | Typical threat here | Typical mitigation |
|---|---|---|
| Prompt injection | User text or web/file content contains instructions that hijack the model | Treat all external text as untrusted data; separate it from instructions; limit what the model can do |
| Sensitive information disclosure | Model reveals personal or confidential data in output | Do not put secrets or unneeded personal data in prompts; filter output; scope retrieval by user |
| Hidden context exposure (earlier name: system prompt leakage) | Hidden prompts or retrieved context read back by a user | Assume prompts are readable; never put secrets in them; enforce access in code, not in prompts |
| Excessive agency | Model-triggered actions with too much power | Least privilege for tools; human confirmation for destructive actions |
| Improper output handling | Model output rendered or executed unsafely (XSS, injection) | Validate, escape, and never execute model output blindly |
| Supply chain | Untrusted models, plugins, or packages | Apply the dependency check to models, plugins, and tools as well |
| Unbounded consumption | Cost or availability abuse | Rate limits, quotas, input and output size caps |

Confirm the current edition and wording at genai.owasp.org before citing.

## Compliance question (ask; do not assume)

If the project handles personal data, children's data, health data, or
payments, ask the person once, in plain words:

> Does this project need to follow any law or policy? For example GDPR (EU/UK),
> India's DPDP Act, children's-privacy rules, health-data rules, card-payment
> rules (PCI DSS), or your university's or employer's rules. Tell me which
> apply, or say "none" or "not sure".

Record the answer under "Rules and policies that apply". If "not sure", add an
open-question marker and suggest they ask their institution or a lawyer. This
is not legal advice and you must not state which laws apply.

Context you may share if India or the DPDP Act comes up: the Digital Personal
Data Protection Act, 2023 and the Digital Personal Data Protection Rules, 2025
(notified in November 2025) are being phased in, with core obligations on
organisations scheduled roughly 18 months after notification (around May
2027) per secondary legal sources. Tell the person to confirm current dates
and applicability with official MeitY or Gazette sources.

## Full track additions

- Every STRIDE row carries an ID (`T-001`...) and a "Verified by" entry for
  **every** status except `Open`. `Planned` rows state the planned check.
- Build-plan traceability (`build-plan.md`) lists the phase for each threat.
- Include a short "Residual risk" paragraph: what remains after mitigations
  and who accepted it.
- Cover each trust boundary from the data-flow diagram at least once.
