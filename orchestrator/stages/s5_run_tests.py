"""
s5_run_tests.py — Stage 5: Test Runner
Runs pytest on ecommerce_stub/tests/ and returns structured results.
"""
import subprocess
import re
import sys
from pathlib import Path


def run(repo_root: Path) -> dict:
    tests_dir = repo_root / "ecommerce_stub" / "tests"
    stub_dir = repo_root / "ecommerce_stub"

    print(f"\n  🔬 Running pytest on ecommerce_stub/tests/\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short", "--no-header"],
        capture_output=True,
        text=True,
        cwd=str(stub_dir),
    )

    output = result.stdout + result.stderr
    test_results = {}

    # Parse individual test results from pytest -v output
    for line in output.splitlines():
        # Match lines like: "tests/test_foo.py::test_bar PASSED" or "FAILED"
        m = re.match(r"\s*(tests/\S+::(\S+))\s+(PASSED|FAILED|ERROR|SKIPPED)", line)
        if m:
            full_id = m.group(1)
            test_name = m.group(2)
            status = m.group(3)
            test_results[test_name] = {"full_id": full_id, "status": status}

    # Summary line — handle both "17 passed, 5 failed" and "5 failed, 17 passed"
    passed_match = re.search(r"(\d+) passed", output)
    failed_match = re.search(r"(\d+) failed", output)
    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0

    # Print a clean summary
    for test_name, info in test_results.items():
        icon = "✅" if info["status"] == "PASSED" else "❌"
        print(f"    {icon}  {test_name}  [{info['status']}]")

    print(f"\n  📊 Results: {passed} passed  |  {failed} failed  |  return code: {result.returncode}\n")

    return {
        "test_results": test_results,
        "passed": passed,
        "failed": failed,
        "returncode": result.returncode,
        "raw_output": output,
    }
