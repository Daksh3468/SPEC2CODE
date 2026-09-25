"""
s6_verify_requirements.py — Stage 6: Requirement Verification
Maps test results back to REQ-IDs and flags unverified requirements.
Writes orchestrator/data/verification_result.json.
"""
import json
from pathlib import Path


def run(repo_root: Path, reqs: list, test_results: dict) -> dict:
    data_dir = repo_root / "orchestrator" / "data"
    data_dir.mkdir(exist_ok=True)

    print(f"\n  🔍 Requirement Verifier — mapping tests → REQ-IDs\n")

    verification = {}
    all_test_names = set(test_results.keys())

    for req in reqs:
        req_id = req["id"]
        req_tests = req.get("test_names", [])
        passing_tests = []
        failing_tests = []
        missing_tests = []

        for t in req_tests:
            if t in all_test_names:
                if test_results[t]["status"] == "PASSED":
                    passing_tests.append(t)
                else:
                    failing_tests.append(t)
            else:
                missing_tests.append(t)

        if failing_tests or missing_tests:
            status = "FAIL"
        elif passing_tests:
            status = "PASS"
        else:
            status = "NO_TESTS"

        verification[req_id] = {
            "title": req["title"],
            "code_symbol": req.get("code_symbol", ""),
            "category": req.get("category", ""),
            "passing_tests": passing_tests,
            "failing_tests": failing_tests,
            "missing_tests": missing_tests,
            "status": status,
        }

        icon = "✅" if status == "PASS" else ("❌" if status == "FAIL" else "⚠️ ")
        test_count = len(passing_tests)
        fail_note = f"  ← {', '.join(failing_tests + missing_tests)}" if failing_tests or missing_tests else ""
        print(f"    {icon}  {req_id}  {req['title']:<42}  {status}  ({test_count} tests){fail_note}")

    fail_count = sum(1 for v in verification.values() if v["status"] != "PASS")
    pass_count = sum(1 for v in verification.values() if v["status"] == "PASS")

    out_file = data_dir / "verification_result.json"
    out_file.write_text(json.dumps(verification, indent=2), encoding="utf-8")

    print(f"\n  📊 Verification: {pass_count} PASS  |  {fail_count} FAIL/MISSING")
    print(f"  💾 Results saved → orchestrator/data/verification_result.json\n")

    return verification
