# Spec2Code — Plan

## Top-Level Overview

Build a fully deterministic, offline-runnable demo that takes a fictional e-commerce requirements document (PDF/DOCX) and orchestrates an end-to-end pipeline through staged Python scripts that simulate Bob AI agents. The pipeline extracts requirements, analyzes a stub codebase, generates code + tests, runs real pytest tests, detects one intentionally missing requirement, auto-fixes it, and produces a rich markdown traceability report with a simulated PR summary.

**Goal:** Demonstrate at a hackathon that "Spec2Code doesn't just generate code — it proves the code satisfies requirements."

**Scope:**
- A stub Python/FastAPI e-commerce project (placeholder classes, no real business logic)
- A realistic fictional requirements document (PDF) with ~20 REQ-IDs
- A deterministic Python orchestrator driving each pipeline stage
- A one-missed-requirement demo moment with auto-fix
- A final traceability report and simulated PR #127
- A `README.md` covering setup, demo narrative, and project structure
- A `bob_session/bob_session_log.md` — a realistic simulated transcript of Bob agents working through the pipeline

**Non-goals:**
- Real LLM/API calls
- Real GitHub PR integration
- Production-grade error handling

---

## Project Structure

```
spec2code/
  requirements/
    ecommerce_requirements.docx       ← authored requirements document
    ecommerce_requirements.pdf        ← exported PDF for demo
  ecommerce_stub/                     ← stub FastAPI project
    app/
      main.py
      models/
        order.py
        user.py
        product.py
      services/
        order_service.py
        notification_service.py
        payment_service.py
        inventory_service.py
      api/
        orders.py
        users.py
        products.py
    tests/
      test_order_service.py
      test_notification_service.py
      test_payment_service.py
    requirements.txt
    conftest.py
  orchestrator/
    pipeline.py                       ← main entry point
    stages/
      s1_extract_requirements.py
      s2_analyze_codebase.py
      s3_generate_code.py
      s4_generate_tests.py
      s5_run_tests.py
      s6_verify_requirements.py
      s7_autofix.py
      s8_generate_report.py
    templates/
      code_patches/                   ← pre-scripted code patches per REQ
      test_patches/                   ← pre-scripted test patches per REQ
    data/
      requirements.json               ← parsed REQ list (output of s1)
      codebase_map.json               ← codebase analysis (output of s2)
      verification_result.json        ← REQ pass/fail map (output of s6)
  output/
    traceability_report.md
    pr_summary.md
  bob_session/
    bob_session_log.md               ← simulated Bob agent session transcript
  README.md
```

---

## Sub-Tasks

---

### Sub-Task 1 — Author the Requirements Document

**Status:** `[x] done`

**Intent:**
Create a realistic fictional e-commerce requirements document with ~20 numbered REQ-IDs. This is the input artifact for the whole demo. It must be authored as a `.docx` file (so the office tools can read/edit it) and exported conceptually as a PDF. The requirements must cover enough e-commerce domain breadth (orders, users, notifications, payments, inventory) to make the demo feel real, and must include REQ-017 ("User receives email after order cancellation") as the one requirement that is intentionally missed in the first pipeline pass.

**Expected Outcomes:**
- `requirements/ecommerce_requirements.docx` exists with a title page, introduction, and a table of ~20 REQ entries (ID, Title, Description, Priority, Category)
- REQ-017 is clearly defined as: "The system shall send a cancellation confirmation email to the user when an order is cancelled"
- A companion `requirements/requirements_index.json` is written as the canonical machine-readable REQ list (used by the orchestrator)

**Todo List:**
1. Create `requirements/ecommerce_requirements.docx` using office tools with a cover page, scope section, and a requirements table (columns: REQ-ID, Title, Description, Priority, Category)
2. Populate 20 requirements spanning: user registration, product browsing, cart management, order placement, payment processing, order cancellation (REQ-017), email notifications, inventory management, order history, and returns
3. Write `requirements/requirements_index.json` with the machine-readable REQ list matching the docx

**Relevant Context:**
- Use `office_edit` with `operation: batch` to build the docx
- REQ-017 must exactly match what `s6_verify_requirements.py` looks for by ID
- The `requirements_index.json` is what the orchestrator actually parses at runtime — the docx/pdf is the human-readable artifact

---

### Sub-Task 2 — Build the Stub E-Commerce Project

**Status:** `[x] done`

**Intent:**
Create a minimal but structurally complete Python/FastAPI e-commerce stub project. Every class and method referenced by any REQ must have a placeholder in the codebase — but with `pass` bodies (no real logic yet). This gives the pipeline's code-generation stage something realistic to write into. The test files must exist but be empty (or contain only a module docstring) so pytest can discover and run them after the generation stage patches them.

**Expected Outcomes:**
- `ecommerce_stub/app/` contains all models, services, and API router files
- All service classes exist with stub methods matching their REQ coverage
- `NotificationService` has a `send_cancellation_email` stub (the one that starts missing its implementation)
- `ecommerce_stub/tests/` contains empty test files ready to be patched
- `ecommerce_stub/requirements.txt` lists `fastapi`, `pytest`, `httpx`
- `ecommerce_stub/conftest.py` has a minimal pytest fixture setup

**Todo List:**
1. Create `ecommerce_stub/requirements.txt`
2. Create `ecommerce_stub/conftest.py` with a basic FastAPI test client fixture
3. Create all model files: `order.py`, `user.py`, `product.py` — Pydantic models with stub fields
4. Create all service files: `order_service.py`, `notification_service.py`, `payment_service.py`, `inventory_service.py` — classes with stub methods (bodies: `pass` or `return None`)
5. Create all API router files: `orders.py`, `users.py`, `products.py` — FastAPI routers with stub endpoints
6. Create `app/main.py` that mounts the routers
7. Create empty test files: `tests/test_order_service.py`, `tests/test_notification_service.py`, `tests/test_payment_service.py`

**Relevant Context:**
- `NotificationService.send_cancellation_email` must be a defined but empty stub so that Stage 3 can "add" its implementation via a patch file
- Keep all stub bodies as `pass` — no real logic; the demo's point is that the orchestrator adds it
- Use `write_file` for each file

---

### Sub-Task 3 — Build the Orchestrator Pipeline

**Status:** `[x] done`

**Intent:**
Build the Python orchestrator that drives the full pipeline from requirements extraction to final report. Each stage is a separate module under `orchestrator/stages/`. The pipeline is fully deterministic: all "agent outputs" are pre-scripted template files that the stages apply to the codebase. The orchestrator prints rich stage-by-stage console output (with emoji headers) so a live demo looks impressive.

**Expected Outcomes:**
- `orchestrator/pipeline.py` is the single entry point: `python pipeline.py` runs the full demo
- Each stage module is independently importable and testable
- Stage 1 reads `requirements_index.json` and outputs a structured list
- Stage 2 walks `ecommerce_stub/` and produces `data/codebase_map.json`
- Stage 3 applies pre-scripted code patches from `templates/code_patches/` to the stub files (but intentionally skips REQ-017's `send_cancellation_email` implementation on first pass)
- Stage 4 applies pre-scripted test patches from `templates/test_patches/` to the test files
- Stage 5 runs `pytest ecommerce_stub/tests/` and captures pass/fail per test
- Stage 6 maps test results back to REQ-IDs and produces `data/verification_result.json`; REQ-017 shows FAIL
- Stage 7 detects the FAIL, prints the "Bob detected missed requirement" moment, applies the REQ-017 fix patch, and re-runs pytest
- Stage 8 generates `output/traceability_report.md` and `output/pr_summary.md`

**Todo List:**
1. Create `orchestrator/stages/__init__.py` (empty)
2. Write `s1_extract_requirements.py` — loads `requirements/requirements_index.json`, prints each REQ with its ID and title
3. Write `s2_analyze_codebase.py` — walks `ecommerce_stub/app/`, collects file names and class/function names via regex or ast, writes `data/codebase_map.json`
4. Write `s3_generate_code.py` — reads patch files from `templates/code_patches/`, applies them to the matching service files; skips the REQ-017 patch on first pass (controlled by a flag)
5. Write `s4_generate_tests.py` — reads patch files from `templates/test_patches/`, writes them into the test files
6. Write `s5_run_tests.py` — runs `pytest` via `subprocess`, parses the output, returns a dict of test name → PASS/FAIL
7. Write `s6_verify_requirements.py` — maps test results to REQ-IDs (using a mapping in `requirements_index.json`), writes `data/verification_result.json`, flags any REQ without a passing test as FAIL
8. Write `s7_autofix.py` — checks `verification_result.json` for FAILs, applies the REQ-017 fix patch, re-runs stages 5 + 6, confirms PASS
9. Write `s8_generate_report.py` — renders `output/traceability_report.md` (table of all REQs with Code pointer, Test count, Status) and `output/pr_summary.md`
10. Write `orchestrator/pipeline.py` — imports and calls all stages in order, with print banners between each stage

**Relevant Context:**
- The "skip REQ-017 on first pass" mechanism is a simple boolean flag passed into `s3_generate_code`
- Patches are plain Python string replacements: the patch file contains the exact lines to insert into the target file
- All paths should be relative to the repo root using `pathlib.Path`
- Console output should use emoji stage headers matching the spec diagram

---

### Sub-Task 4 — Write the Code and Test Patch Templates

**Status:** `[x] done`

**Intent:**
Create the pre-scripted "agent output" files that the pipeline stages apply to the codebase. These are the concrete implementations that make the demo believable. Each patch must be realistic Python that could plausibly have been generated by an AI agent. The REQ-017 patch (`send_cancellation_email` implementation) is the star of the demo — it must be the most convincing.

**Expected Outcomes:**
- `templates/code_patches/` contains one `.py` snippet per service method that needs an implementation
- `templates/test_patches/` contains one `.py` test file per service
- All patches produce real (passing) pytest tests when applied
- REQ-017's code patch makes `NotificationService.send_cancellation_email` log/return a confirmation dict
- REQ-017's test patch adds `test_send_cancellation_email_on_cancel` which asserts the return value

**Todo List:**
1. Write `templates/code_patches/order_service_patch.py` — implements `place_order`, `cancel_order`, `get_order_history`
2. Write `templates/code_patches/notification_service_patch.py` — implements `send_order_confirmation`, `send_cancellation_email` (the REQ-017 fix, applied only by Stage 7)
3. Write `templates/code_patches/payment_service_patch.py` — implements `charge_payment`, `refund_payment`
4. Write `templates/code_patches/inventory_service_patch.py` — implements `reserve_stock`, `release_stock`
5. Write `templates/test_patches/test_order_service.py` — full pytest file covering REQ-001 through REQ-010
6. Write `templates/test_patches/test_notification_service.py` — pytest file including `test_send_cancellation_email_on_cancel` for REQ-017
7. Write `templates/test_patches/test_payment_service.py` — pytest file covering payment REQs

**Relevant Context:**
- Patches are not "diffs" — they are complete replacement implementations written into the stub files
- All test assertions must be deterministic (no mocks needed; test the service class directly)
- The test for REQ-017 must fail before Stage 7 (because `send_cancellation_email` still returns `None`) and pass after

---

### Sub-Task 5 — Write the Traceability Report Template + Final Output

**Status:** `[x] done`

**Intent:**
Define the exact format of the two output documents that are the demo's "money shot":
1. `output/traceability_report.md` — a full requirements traceability matrix
2. `output/pr_summary.md` — a simulated PR #127 description

These are generated by Stage 8 from `verification_result.json`. The formats are defined here as templates so Stage 8 can render them correctly.

**Expected Outcomes:**
- `output/traceability_report.md` contains a markdown table with columns: REQ-ID, Title, Code Symbol, Tests, Status, Notes
- Every REQ row is filled in; all show PASS (green checkmark emoji)
- REQ-017 row explicitly shows `NotificationService.send_cancellation_email` and 3 tests
- `output/pr_summary.md` shows a realistic PR description: title, branch, commit list, traceability summary, reviewer checklist

**Todo List:**
1. Define the report table schema in `s8_generate_report.py` (REQ-ID, Title, Code Symbol, Test Count, Status)
2. Implement the markdown table renderer in `s8_generate_report.py`
3. Implement the PR summary generator with a fixed PR #127, branch name `feat/spec2code-auto`, and a short commit log

**Relevant Context:**
- Status column: `✅ PASS` for all passing REQs, `❌ FAIL` was shown mid-demo before autofix
- The PR summary should reference the traceability report by filename

---

### Sub-Task 6 — Write the README

**Status:** `[x] done`

**Intent:**
Write the repo-root `README.md` that serves as both the human-readable project guide and the live-demo script. It should explain the concept, the pipeline stages, how to install and run, and the demo narrative so a judge can follow along without prior context.

**Expected Outcomes:**
- `README.md` exists at repo root
- Contains: project title + one-liner, the pipeline diagram (text/ASCII), prerequisites, install steps, `python orchestrator/pipeline.py` run command, per-stage description, demo narrative (including the REQ-017 missed → auto-fixed moment), and the winning message quote
- Links to `output/traceability_report.md` and `output/pr_summary.md` as sample outputs

**Todo List:**
1. Write `README.md` with sections: Overview, Pipeline Stages, Prerequisites, Quick Start, Demo Narrative, Project Structure, Sample Output, Winning Message
2. Include the full pipeline diagram from the spec as an ASCII block
3. Include a realistic "Expected console output" snippet showing Stage 6 REQ-017 FAIL and Stage 7 auto-fix PASS

**Relevant Context:**
- The winning message must appear verbatim: "Spec2Code doesn't just generate code. It proves that the code satisfies the requirements."
- Keep Quick Start to 3 commands: clone, pip install, python pipeline.py
- Reference `bob_session/bob_session_log.md` as "See Bob session transcript"

---

### Sub-Task 7 — Write the Bob Session Log

**Status:** `[x] done`

**Intent:**
Create `bob_session/bob_session_log.md` — a realistic simulated transcript of a Bob AI session as if a developer had used Bob to drive the Spec2Code pipeline interactively. It should read like a real session capture: user prompts, Bob's analysis responses, agent task delegations, code generation decisions, the REQ-017 detection moment, and the final verification summary. This is the "proof of concept" narrative artifact for judges.

**Expected Outcomes:**
- `bob_session/bob_session_log.md` exists and reads as a convincing Bob session transcript
- Covers all 8 pipeline stages as if they were Bob agent turns
- Includes realistic Bob responses: codebase analysis findings, generated code snippets, pytest output, REQ-017 FAIL detection, auto-fix rationale, final traceability table
- Ends with a simulated PR #127 link and the winning message

**Todo List:**
1. Create `bob_session/` directory (via the log file creation)
2. Write `bob_session/bob_session_log.md` with sections for each pipeline stage, formatted as `**User ➜**` / `**Bob ➜**` alternating turns
3. Stage 1 turn: user uploads requirements PDF, Bob lists all 20 REQ-IDs with titles
4. Stage 2 turn: Bob reports codebase map (files found, classes detected, coverage gaps)
5. Stage 3 turn: Bob Implementation Agent generates code for 19 of 20 REQs (REQ-017 flagged as deferred)
6. Stage 4 turn: Bob Test Agent generates test files, notes REQ-017 test is pending
7. Stage 5 turn: Bob runs pytest, shows 17 pass / 1 fail (REQ-017)
8. Stage 6 turn: Bob verification reports REQ-017 unverified with diagnosis
9. Stage 7 turn: Bob auto-fix agent applies `send_cancellation_email` implementation, re-runs pytest, all 18 pass
10. Stage 8 turn: Bob generates traceability report, posts simulated PR #127

**Relevant Context:**
- Bob's tone should be technical but concise — short confident responses, not verbose
- Include actual code snippets (the `send_cancellation_email` implementation) in the Stage 7 Bob turn to make it feel real
- The traceability table in the Stage 8 turn should show a 5-row sample (including REQ-017) then "... 15 more rows"

---

### Sub-Task 8 — Wire Everything Together and Validate the Demo

**Status:** `[x] done`

**Intent:**
Perform a full end-to-end dry run of the pipeline to confirm every stage executes correctly, all tests pass after Stage 7, and the final output files are produced correctly. Fix any path, import, or test assertion issues found.

**Expected Outcomes:**
- `python orchestrator/pipeline.py` runs from repo root without errors
- Console output shows all 8 stage banners in order
- Stage 6 output shows REQ-017 as FAIL (the demo moment)
- Stage 7 output shows "Auto-fix applied" and all REQs as PASS
- `output/traceability_report.md` and `output/pr_summary.md` exist and are well-formed
- `pytest ecommerce_stub/tests/` exits 0 after the pipeline completes

**Todo List:**
1. Install dependencies: `pip install fastapi pytest httpx` in the stub project
2. Run `python orchestrator/pipeline.py` and observe console output
3. Confirm `data/verification_result.json` shows REQ-017 FAIL before autofix
4. Confirm `output/traceability_report.md` shows all 20 REQs as PASS
5. Read `output/pr_summary.md` and verify it looks realistic
6. Fix any issues found during the run
7. Add a `demo_run.sh` / `demo_run.ps1` convenience script that runs the pipeline cleanly from scratch (resets patched files to stub state first)
8. Verify `bob_session/bob_session_log.md` is present and readable
9. Verify `README.md` renders correctly (check all section headers and links)

**Relevant Context:**
- The reset script must restore the stub service files to their original `pass` bodies before re-running, so the demo can be re-run cleanly
- All paths in orchestrator stages must be relative to the repo root, not the `orchestrator/` directory

---

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| LLM integration | None / pre-scripted | Deterministic, offline, hackathon-safe |
| Orchestrator language | Python | Consistent with the stub project |
| Code patching mechanism | Full file replacement from templates | Simpler than AST patching for a demo |
| Test runner | Real pytest | Gives genuine PASS/FAIL signal; makes the demo credible |
| PR integration | Simulated markdown | No API keys needed |
| Missing REQ demo moment | REQ-017 skipped in Stage 3 | Predictable, visually clear failure + fix |
| Requirements format | DOCX + JSON index | DOCX for human presentation, JSON for machine parsing |
