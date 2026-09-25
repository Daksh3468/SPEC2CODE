"""
s1_extract_requirements.py — Stage 1: Requirement Extraction
Reads requirements/requirements_index.json and returns a structured list of REQs.
"""
import json
from pathlib import Path


def run(repo_root: Path) -> list:
    req_file = repo_root / "requirements" / "requirements_index.json"
    data = json.loads(req_file.read_text(encoding="utf-8"))
    reqs = data["requirements"]

    print(f"\n  📋 Project: {data['project']}  |  Version: {data['version']}")
    print(f"  Found {len(reqs)} requirements:\n")
    for r in reqs:
        priority_tag = f"[{r['priority'].upper()}]"
        print(f"    {r['id']}  {priority_tag:<8}  {r['title']}")
    print()
    return reqs
