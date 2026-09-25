"""
s2_analyze_codebase.py — Stage 2: Codebase Analysis
Walks ecommerce_stub/app/, collects file structure and class/function names,
writes orchestrator/data/codebase_map.json.
"""
import ast
import json
from pathlib import Path


def _extract_symbols(filepath: Path) -> dict:
    """Parse a Python file and extract top-level classes and their methods."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except SyntaxError:
        return {"classes": [], "functions": []}

    classes = []
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
            classes.append({"name": node.name, "methods": methods})
        elif isinstance(node, ast.FunctionDef) and not any(
            isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)
            if hasattr(parent, "body") and node in getattr(parent, "body", [])
        ):
            functions.append(node.name)

    return {"classes": classes, "functions": functions}


def run(repo_root: Path) -> dict:
    stub_dir = repo_root / "ecommerce_stub" / "app"
    codebase_map = {}

    py_files = sorted(stub_dir.rglob("*.py"))
    print(f"\n  🔍 Scanning {len(py_files)} Python files in ecommerce_stub/app/\n")

    for filepath in py_files:
        rel = filepath.relative_to(repo_root)
        symbols = _extract_symbols(filepath)
        codebase_map[str(rel)] = symbols
        class_names = [c["name"] for c in symbols["classes"]]
        if class_names:
            print(f"    {rel}  →  classes: {', '.join(class_names)}")

    # Write codebase map
    data_dir = repo_root / "orchestrator" / "data"
    data_dir.mkdir(exist_ok=True)
    out = data_dir / "codebase_map.json"
    out.write_text(json.dumps(codebase_map, indent=2), encoding="utf-8")

    total_classes = sum(len(v["classes"]) for v in codebase_map.values())
    total_methods = sum(len(c["methods"]) for v in codebase_map.values() for c in v["classes"])
    print(f"\n  📊 Summary: {len(codebase_map)} files  |  {total_classes} classes  |  {total_methods} stub methods")
    print(f"  💾 Codebase map saved → orchestrator/data/codebase_map.json\n")
    return codebase_map
