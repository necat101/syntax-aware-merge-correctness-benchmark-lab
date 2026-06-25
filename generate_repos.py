#!/usr/bin/env python3
"""
Generate reproducible synthetic git histories for merge testing.
Creates base/ours/theirs branches with planted merge scenarios.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("test-repos")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd, cwd=None, check=True):
    """Run shell command"""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result

def init_repo(path):
    """Initialize git repo with initial commit"""
    path.mkdir(parents=True, exist_ok=True)
    run_cmd("git init -b main", cwd=path)
    run_cmd("git config user.email 'test@example.com'", cwd=path)
    run_cmd("git config user.name 'Test User'", cwd=path)
    return path

def write_and_commit(repo_path, files, message):
    """Write files and commit"""
    for filepath, content in files.items():
        full_path = repo_path / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    run_cmd("git add -A", cwd=repo_path)
    run_cmd(f"git commit -m '{message}'", cwd=repo_path)

def create_scenario_01():
    """Different functions - should merge cleanly"""
    repo = init_repo(OUTPUT_DIR / "01-different-functions")
    
    # Base
    write_and_commit(repo, {
        "math.py": "def add(a, b):\n    return a + b\n\ndef multiply(a, b):\n    return a * b\n"
    }, "Initial")
    
    # Ours
    run_cmd("git checkout -b ours", cwd=repo)
    write_and_commit(repo, {
        "math.py": "def add(a, b):\n    # Type check\n    return a + b\n\ndef multiply(a, b):\n    return a * b\n"
    }, "Add comment to add")
    
    # Theirs
    run_cmd("git checkout main", cwd=repo)
    run_cmd("git checkout -b theirs", cwd=repo)
    write_and_commit(repo, {
        "math.py": "def add(a, b):\n    return a + b\n\ndef multiply(a, b):\n    # Overflow check\n    return a * b\n"
    }, "Add comment to multiply")
    
    return repo

def create_scenario_02():
    """Same function - should conflict"""
    repo = init_repo(OUTPUT_DIR / "02-same-function")
    
    write_and_commit(repo, {
        "utils.py": "def format_name(first, last):\n    return f\"{first} {last}\"\n"
    }, "Initial")
    
    run_cmd("git checkout -b ours", cwd=repo)
    write_and_commit(repo, {
        "utils.py": "def format_name(first, last):\n    return f\"{last}, {first}\"\n"
    }, "Ours: last, first")
    
    run_cmd("git checkout main", cwd=repo)
    run_cmd("git checkout -b theirs", cwd=repo)
    write_and_commit(repo, {
        "utils.py": "def format_name(first, last):\n    return f\"{first} {last}\".upper()\n"
    }, "Theirs: uppercase")
    
    return repo

def create_scenario_03():
    """Adjacent edits"""
    repo = init_repo(OUTPUT_DIR / "03-adjacent-edits")
    
    write_and_commit(repo, {
        "config.py": "DEBUG = False\nPORT = 8080\nHOST = 'localhost'\n"
    }, "Initial")
    
    run_cmd("git checkout -b ours", cwd=repo)
    write_and_commit(repo, {
        "config.py": "DEBUG = False\nPORT = 9000\nHOST = 'localhost'\n"
    }, "Ours: port 9000")
    
    run_cmd("git checkout main", cwd=repo)
    run_cmd("git checkout -b theirs", cwd=repo)
    write_and_commit(repo, {
        "config.py": "DEBUG = False\nPORT = 8080\nHOST = '0.0.0.0'\n"
    }, "Theirs: host 0.0.0.0")
    
    return repo

def main():
    print("Generating test repositories...")
    
    scenarios = [
        ("01-different-functions", create_scenario_01),
        ("02-same-function", create_scenario_02),
        ("03-adjacent-edits", create_scenario_03),
    ]
    
    results = []
    for name, func in scenarios:
        try:
            repo = func()
            print(f"✓ {name}")
            results.append({"name": name, "status": "ok", "path": str(repo)})
        except Exception as e:
            print(f"✗ {name}: {e}")
            results.append({"name": name, "status": "failed", "error": str(e)})
    
    # Save manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "scenarios": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["status"] == "ok")
    }
    
    with open(OUTPUT_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nGenerated {manifest['successful']}/{manifest['total']} scenarios")

if __name__ == "__main__":
    main()
