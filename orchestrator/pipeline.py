"""
pipeline.py — Spec2Code main orchestration entry point.

Usage:
    python orchestrator/pipeline.py

Runs all 8 pipeline stages end-to-end, demonstrating:
  PDF → Requirement extraction → Codebase analysis → Code generation →
  Test generation → Test run → Requirement verification →
  Auto-fix (REQ-017) → Traceability report → Verified PR

"""
import sys
import io
import time
from pathlib import Path

# Force UTF-8 output on Windows (handles emoji in console banners)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Ensure repo root is on sys.path so orchestrator and ecommerce_stub are importable
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from orchestrator.stages import (
    s1_extract_requirements,
    s2_analyze_codebase,
    s3_generate_code,
    s4_generate_tests,
    s5_run_tests,
    s6_verify_requirements,
    s7_autofix,
    s8_generate_report,
)

BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║              🚀  SPEC2CODE  —  Requirements → Verified PR       ║
║         Orchestrated by IBM Bob  |  ShopFlow E-Commerce v1.0    ║
╚══════════════════════════════════════════════════════════════════╝
"""

STAGE_BANNERS = {
    1: "📄  STAGE 1 — Analyze & Extract Requirements",
    2: "🏗   STAGE 2 — Analyze Existing Codebase",
    3: "🤖  STAGE 3 — Parallel Bob Agents: Code Generation",
    4: "🧪  STAGE 4 — Parallel Bob Agents: Test Generation",
    5: "🔬  STAGE 5 — Run Tests",
    6: "🔍  STAGE 6 — Requirement Verification",
    7: "⚡  STAGE 7 — Auto-Fix: Missed Requirement Detected",
    8: "✅  STAGE 8 — Traceability Report + Verified PR",
}


def _stage(n: int) -> None:
    banner = STAGE_BANNERS[n]
    width = 66
    separator = "─" * width
    print(f"\n{separator}")
    print(f"  {banner}")
    print(separator)


def _reset_for_demo(repo_root: Path) -> None:
    """Reset the notification service to its stub state so the demo always shows REQ-017 failing."""
    import shutil
    stub_src = repo_root / "orchestrator" / "templates" / "stubs" / "notification_service_stub.py"
    stub_dst = repo_root / "ecommerce_stub" / "app" / "services" / "notification_service.py"
    shutil.copy2(stub_src, stub_dst)

    # Also reset test files to empty stubs so Stage 4 applies them fresh
    tests_dir = repo_root / "ecommerce_stub" / "tests"
    for test_name in ["test_order_service", "test_notification_service", "test_payment_service"]:
        test_file = tests_dir / f"{test_name}.py"
        test_file.write_text(f'"""Auto-reset stub — populated by Spec2Code Stage 4."""\n', encoding="utf-8")


def main():
    print(BANNER)
    time.sleep(0.3)

    # Reset files to stub state so the demo always hits REQ-017 failure
    _reset_for_demo(REPO_ROOT)

    # ── Stage 1: Extract requirements ────────────────────────────────────────
    _stage(1)
    reqs = s1_extract_requirements.run(REPO_ROOT)
    time.sleep(0.2)

    # ── Stage 2: Analyze codebase ─────────────────────────────────────────────
    _stage(2)
    codebase_map = s2_analyze_codebase.run(REPO_ROOT)
    time.sleep(0.2)

    # ── Stage 3: Code generation (REQ-017 intentionally skipped) ─────────────
    _stage(3)
    s3_generate_code.run(REPO_ROOT, apply_req_017=False)
    time.sleep(0.2)

    # ── Stage 4: Test generation ──────────────────────────────────────────────
    _stage(4)
    s4_generate_tests.run(REPO_ROOT)
    time.sleep(0.2)

    # ── Stage 5: Run tests ────────────────────────────────────────────────────
    _stage(5)
    test_run = s5_run_tests.run(REPO_ROOT)
    time.sleep(0.2)

    # ── Stage 6: Verify requirements ──────────────────────────────────────────
    _stage(6)
    verification = s6_verify_requirements.run(REPO_ROOT, reqs, test_run["test_results"])
    time.sleep(0.2)

    # Check if any requirements failed
    failed = [req_id for req_id, v in verification.items() if v["status"] != "PASS"]
    if failed:
        print(f"\n  💥 ALERT: {len(failed)} requirement(s) unverified — invoking Auto-Fix Agent...")

        # ── Stage 7: Auto-fix ─────────────────────────────────────────────────
        _stage(7)
        verification = s7_autofix.run(REPO_ROOT, verification, reqs)
        time.sleep(0.2)
    else:
        print(f"\n  ✅ All requirements verified on first pass — no auto-fix needed.\n")

    # ── Stage 8: Generate report + PR ─────────────────────────────────────────
    _stage(8)
    s8_generate_report.run(REPO_ROOT, verification, reqs)

    # ── Final summary ─────────────────────────────────────────────────────────
    total = len(verification)
    passing = sum(1 for v in verification.values() if v["status"] == "PASS")
    print("─" * 66)
    print(f"""
  🏁  PIPELINE COMPLETE

  Requirements:  {total} total  |  {passing} verified  |  {total - passing} unverified
  Output files:
    → output/traceability_report.md
    → output/pr_summary.md
    → orchestrator/data/verification_result.json
    → orchestrator/data/codebase_map.json

  Simulated PR:  #127  feat/spec2code-auto → main

  ┌─────────────────────────────────────────────────────────────────┐
  │  "Spec2Code doesn't just generate code.                         │
  │   It proves that the code satisfies the requirements."          │
  └─────────────────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    main()
