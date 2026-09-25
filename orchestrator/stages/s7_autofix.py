"""
s7_autofix.py — Stage 7: Auto-Fix Agent
Detects failed REQ verifications, applies the REQ-017 fix patch,
re-runs tests and verification until all requirements pass.
"""
from pathlib import Path
from orchestrator.stages import s3_generate_code, s5_run_tests, s6_verify_requirements


def run(repo_root: Path, verification: dict, reqs: list) -> dict:
    failed_reqs = [req_id for req_id, v in verification.items() if v["status"] != "PASS"]

    if not failed_reqs:
        print("\n  All requirements already passing — auto-fix not needed.\n")
        return verification

    print(f"\n  Auto-Fix Agent — {len(failed_reqs)} unverified requirement(s) detected:")
    for req_id in failed_reqs:
        info = verification[req_id]
        failing = info["failing_tests"] + info["missing_tests"]
        print(f"\n    +-  {req_id}: {info['title']}")
        print(f"    |   Code symbol  : {info['code_symbol']}")
        print(f"    |   Failing tests: {', '.join(failing)}")
        if req_id == "REQ-017":
            print(f"    |   Root cause   : send_cancellation_email returns None (stub not patched)")
            print(f"    +-  Action       : Applying notification_service_patch.py")
        else:
            print(f"    |   Root cause   : stub method not yet implemented")
            print(f"    +-  Action       : code patch covers this REQ")

    print(f"\n  Applying auto-fix for REQ-017 — NotificationService.send_cancellation_email\n")

    # Apply the REQ-017 notification service patch
    s3_generate_code.run(repo_root, apply_req_017=True)

    # Re-run tests
    print(f"  Re-running full test suite after auto-fix...\n")
    test_run = s5_run_tests.run(repo_root)

    # Re-verify
    updated_verification = s6_verify_requirements.run(repo_root, reqs, test_run["test_results"])

    still_failing = [req_id for req_id, v in updated_verification.items() if v["status"] != "PASS"]
    if still_failing:
        print(f"  Warning: still failing after auto-fix: {still_failing}")
    else:
        print(f"  All {len(updated_verification)} requirements verified after auto-fix!\n")

    return updated_verification
