# Documentation Structure Plan — MiniChain (Group 12)

Planning document only. No files are created or moved by this plan; it is a proposal for review.

---

## 1. Project understanding

**Summary.** MiniChain is a simplified, functional blockchain written in Python for the HKBU course COMP4137/COMP7200 (Group 12). It implements ECC accounts, SISO transactions, a SHA-256 Merkle tree, a block/chain structure, Proof-of-Work mining (difficulty = 4), and tamper-detection via `is_chain_valid()`. Two scripts (`test_phase1.py`, `test_phase2.py`) act as both tests and demonstrations.

**Main purpose.** Course deliverable (Phase II deadline: 2026-04-24). Grading weights code correctness, a written report, README clarity, and reproducibility of outputs.

**Likely user types.**
- **Graders / TAs** — need to install, run the two test scripts, and match observed output to the reproducibility table.
- **Group members** — need shared reference for architecture, design rationale, and member roles for the report.
- **AI assistants (Claude Code, etc.)** — need a compact, navigable index (files, responsibilities, entry points) to help edit or extend code without re-scanning the repo.
- **Future students / readers** — may use this as a study reference for blockchain internals.

---

## 2. Current content audit

**What already exists:**
- `readme.md` — the **course assignment brief** from the instructor (milestones, tasks, grading, deliverable rules). Not a project README.
- `PROJECT_README.md` — the actual **submission README**: abstract, file tree, dependencies, install steps, execution guide, expected output, reproducibility matrix. Member names are blank.
- `src/*.py` — rich module-level and function-level docstrings explaining each component.
- `test_phase1.py`, `test_phase2.py` — executable demos with printed section separators that function as informal tutorials.
- `requirements.txt`, `.gitignore` — standard.

**Content mixed together that should be separated:**
- `PROJECT_README.md` bundles *abstract + install + execution guide + expected output + reproducibility matrix* in one file. Install/run belongs in README; detailed expected output and the experiment matrix are long enough to warrant their own docs.
- `readme.md` is misnamed — it is the *course spec*, not a project readme. Keeping it at the top level under that filename will mislead both humans and AI tools (most tools auto-load `readme.md` as the project intro).
- Architecture and design rationale currently live **only inside docstrings**. This works for developers reading code but is invisible to anyone skimming the repo, and fragments the big-picture view across five files.

**Content missing:**
- Central **architecture overview** (component diagram / data-flow description: Account → Transaction → Merkle → Block → Chain).
- **Design rationale** (why SECP256K1, why SHA-256, why difficulty = 4, why fixed genesis timestamp, why `tx_id` is computed once).
- **Testing strategy** — which attack each tamper step simulates and why detection works.
- **Contributors / member roles** — the report requires per-member work distribution; `PROJECT_README.md` has an empty "Members:" line.
- **AI-readable index** (`llms.txt`) pointing to the key files and their purposes.
- A brief **troubleshooting / known-quirks** note (e.g., mining time variance, Windows emoji console rendering).

---

## 3. Proposed documentation structure

```
Blockchain_project_group12-main/
├── README.md                  ← renamed + trimmed from PROJECT_README.md
├── llms.txt                   ← AI-readable index
├── requirements.txt
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md        ← system overview, components, data flow
│   ├── DESIGN.md              ← algorithm choices & rationale
│   ├── USAGE.md               ← detailed run guide + full expected output
│   ├── TESTING.md             ← test strategy + tamper-detection explanations
│   ├── REPRODUCIBILITY.md     ← experiment matrix (moved from README)
│   ├── CONTRIBUTORS.md        ← group members + work distribution
│   └── COURSE_SPEC.md         ← renamed from top-level readme.md
├── src/
│   └── ... (unchanged)
├── test_phase1.py
└── test_phase2.py
```

**Reason for each file:**
- `README.md` — canonical first-read; what tools and graders open by default. Keep short.
- `llms.txt` — emerging convention for exposing structured pointers to LLMs; helps AI assistants locate relevant files without grep-scanning.
- `docs/ARCHITECTURE.md` — the "big picture" the code's docstrings never assemble.
- `docs/DESIGN.md` — rationale graders will look for in the report; drafting it here makes report-writing easier.
- `docs/USAGE.md` — keeps the long expected-output blocks out of README.
- `docs/TESTING.md` — explains *why* each tamper is detected, which is explicitly required by the spec (§5.5).
- `docs/REPRODUCIBILITY.md` — required artifact section (§7). Separating makes graders' check-off easier.
- `docs/CONTRIBUTORS.md` — fills the empty "Members:" gap and mirrors the report's contribution section.
- `docs/COURSE_SPEC.md` — preserves the instructor brief for reference without hijacking the `readme.md` slot.

---

## 4. Content plan for each file

### README.md
- **Purpose:** fast onboarding; what the project is, how to install, how to run.
- **Include:** one-paragraph abstract, badges/phase status, short file-tree, install (3 steps), quick-start commands (`python test_phase1.py`, `python test_phase2.py`), link table to every `docs/` file.
- **Exclude:** full expected output blocks, reproducibility matrix, design rationale, course-spec reprint, member bios.

### llms.txt
- **Purpose:** compact, flat index for LLM agents.
- **Include:** project title, one-line summary, key entry-point files with one-line descriptions (`src/account.py`, `src/transaction.py`, ..., `test_phase1.py`, `test_phase2.py`), links to each `docs/*.md`, notable constants (e.g., `DIFFICULTY = 4`).
- **Exclude:** narrative prose, install steps (link to README instead), duplicated docstrings.

### docs/ARCHITECTURE.md
- **Purpose:** big-picture structural view.
- **Include:** ASCII component diagram (Account → Transaction → MerkleTree → Block → Blockchain), responsibility table per module, data-flow walkthrough for "create chain → mine block → verify chain", class/function map with file:line anchors.
- **Exclude:** install instructions, algorithm derivations, per-line code.

### docs/DESIGN.md
- **Purpose:** explain *why* each choice was made.
- **Include:** ECC curve choice (SECP256K1), hash algorithm (SHA-256), PoW difficulty selection (4), fixed-zero genesis timestamp rationale, why `tx_id` is frozen at construction, Merkle power-of-2 assumption, trade-offs and known limitations.
- **Exclude:** step-by-step run commands, large code snippets, team roles.

### docs/USAGE.md
- **Purpose:** detailed execution reference.
- **Include:** full Phase I and Phase II expected output blocks, flag/environment notes, estimated runtimes, Windows-vs-Unix command variants, how to tweak difficulty for faster demos.
- **Exclude:** architecture narrative, design rationale.

### docs/TESTING.md
- **Purpose:** document the tests and why tamper detection works.
- **Include:** test inventory (what each `test_*.py` covers), per-attack walkthroughs (tamper tx amount, tamper block header, break prev-hash link, tamper genesis) with the mechanism that catches each, how to add new tests.
- **Exclude:** install steps, design rationale unrelated to detection.

### docs/REPRODUCIBILITY.md
- **Purpose:** satisfy the artifact evaluation rubric (§7 of the course spec).
- **Include:** hardware/OS/software matrix, install/compile time estimates, execution time estimates, experiment-to-result mapping table (already drafted in `PROJECT_README.md`), stdout-vs-report correspondence.
- **Exclude:** source code reproductions, narrative architecture.

### docs/CONTRIBUTORS.md
- **Purpose:** record team members and per-member work distribution.
- **Include:** names, student IDs, per-member responsibilities mapped to files/phases, acknowledgements of external resources.
- **Exclude:** install or usage steps.
- **Note:** content must be supplied by the group — see §6.

### docs/COURSE_SPEC.md
- **Purpose:** preserve the instructor's brief verbatim for reference.
- **Include:** current contents of `readme.md` unchanged, plus a one-line header noting this is the instructor-provided assignment.
- **Exclude:** anything written by the group (that belongs in other docs).

---

## 5. Priority order

**Create first (needed before submission on 2026-04-24):**
1. `README.md` (rename + trim `PROJECT_README.md`) — graders' first stop.
2. `docs/COURSE_SPEC.md` (rename `readme.md`) — frees the `README.md` slot without losing the brief.
3. `docs/CONTRIBUTORS.md` — required by report; currently blank.
4. `docs/REPRODUCIBILITY.md` — explicitly graded (§7).
5. `docs/USAGE.md` — receives the expected-output content extracted from the old README.

**Create second (improves quality but not blocking):**
6. `docs/ARCHITECTURE.md` — useful to paste into the report.
7. `docs/TESTING.md` — supports the tamper-detection explanation the spec requires.
8. `docs/DESIGN.md` — supports the report's Design & Implementation section.

**Optional / nice-to-have:**
9. `llms.txt` — helpful for future AI-assisted edits; not required by the rubric.

---

## 6. Risks / notes

**Unclear areas (need human confirmation):**
- **Member list and student IDs** are blank in `PROJECT_README.md`. `docs/CONTRIBUTORS.md` cannot be completed without the group filling these in.
- **Per-member work distribution** is required by both the report and `CONTRIBUTORS.md` but is not derivable from the codebase. Must be supplied manually.
- **Citations / external references** used in coding (e.g., any copied snippets) are not listed anywhere yet; the spec warns on plagiarism, so any borrowed code should be recorded before submission.

**Assumptions made from current project state:**
- The top-level `readme.md` is the instructor's assignment brief (content and phrasing confirm this) and is not meant to be the project's own README.
- `PROJECT_README.md` is the group's intended submission README and can be safely renamed.
- The project will stay Python-only; no additional languages or build tooling to document.
- No CI or deployment pipeline exists; therefore no CI/deployment docs are proposed.
- `llms.txt` follows the informal emerging convention (plain-text pointers to key docs). If the grader rubric is strict about unexpected files, it can be dropped without loss.

**Places where content may need manual confirmation:**
- Runtime estimates in `USAGE.md` / `REPRODUCIBILITY.md` should be re-measured on the submitting member's machine rather than copied from the current `PROJECT_README.md`.
- Any `docs/DESIGN.md` claims about rationale (e.g., "we chose SECP256K1 because …") must match what the group will write in the final report to avoid inconsistencies.
- The `src/transaction.py` data field currently stores only the amount, while the course spec §5.1 mentions "amount **and** a crypto-hash of the amount." Decide before documenting whether to (a) reflect the current implementation in docs, or (b) implement the missing hash field first and then document. This is a scope decision for the group, not for this plan.

---

*End of plan. No implementation will proceed until the group reviews and approves this structure.*
