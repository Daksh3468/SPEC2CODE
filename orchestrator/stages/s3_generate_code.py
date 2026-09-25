"""
s3_generate_code.py — Stage 3: Code Generation (Implementation Agent)
Applies pre-scripted code patches from templates/code_patches/ to the stub service files.
On first pass, REQ-017 (notification_service_patch) is intentionally skipped.
"""
import shutil
from pathlib import Path


# Map: patch file → target service file (relative to repo root)
CODE_PATCH_MAP = {
    "order_service_patch.py": "ecommerce_stub/app/services/order_service.py",
    "payment_service_patch.py": "ecommerce_stub/app/services/payment_service.py",
    "inventory_service_patch.py": "ecommerce_stub/app/services/inventory_service.py",
}

# REQ-017 patch — applied only by Stage 7 (auto-fix)
REQ_017_PATCH = "notification_service_patch.py"
REQ_017_TARGET = "ecommerce_stub/app/services/notification_service.py"


def run(repo_root: Path, apply_req_017: bool = False) -> list:
    patches_dir = repo_root / "orchestrator" / "templates" / "code_patches"
    applied = []

    print(f"\n  🤖 Implementation Agent — applying code patches\n")

    for patch_name, target_rel in CODE_PATCH_MAP.items():
        src = patches_dir / patch_name
        dst = repo_root / target_rel
        shutil.copy2(src, dst)
        applied.append(target_rel)
        service_name = patch_name.replace("_patch.py", "").replace("_", " ").title()
        print(f"    ✅  {service_name}  →  {target_rel}")

    if apply_req_017:
        src = patches_dir / REQ_017_PATCH
        dst = repo_root / REQ_017_TARGET
        shutil.copy2(src, dst)
        applied.append(REQ_017_TARGET)
        print(f"    ✅  Notification Service (REQ-017 fix)  →  {REQ_017_TARGET}")
    else:
        print(f"    ⏭️  Notification Service  →  DEFERRED (REQ-017 not yet implemented)")

    print(f"\n  📦 {len(applied)} service files patched\n")
    return applied
