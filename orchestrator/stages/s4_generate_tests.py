"""
s4_generate_tests.py — Stage 4: Test Generation Agent
Applies pre-scripted test patches from templates/test_patches/ to the test files.
"""
import shutil
from pathlib import Path


TEST_PATCH_MAP = {
    "test_order_service.py": "ecommerce_stub/tests/test_order_service.py",
    "test_notification_service.py": "ecommerce_stub/tests/test_notification_service.py",
    "test_payment_service.py": "ecommerce_stub/tests/test_payment_service.py",
}


def run(repo_root: Path) -> list:
    patches_dir = repo_root / "orchestrator" / "templates" / "test_patches"
    applied = []

    print(f"\n  🧪 Test Generation Agent — applying test patches\n")

    for patch_name, target_rel in TEST_PATCH_MAP.items():
        src = patches_dir / patch_name
        dst = repo_root / target_rel
        shutil.copy2(src, dst)
        applied.append(target_rel)
        suite_name = patch_name.replace(".py", "").replace("_", " ").title()
        print(f"    ✅  {suite_name}  →  {target_rel}")

    print(f"\n  📋 Note: test_send_cancellation_email_on_cancel (REQ-017) is present but")
    print(f"          will FAIL until NotificationService.send_cancellation_email is implemented.\n")
    return applied
