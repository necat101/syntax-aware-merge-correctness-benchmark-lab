#!/usr/bin/env python3
"""
Generate reproducible synthetic git histories for merge testing.
Creates base/ours/theirs branches with planted ground truth.
"""

import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("test-repos")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd, cwd=None, check=True, timeout=10):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=timeout
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nSTDERR: {result.stderr}")
    return result

def init_repo(path):
    path.mkdir(parents=True, exist_ok=True)
    run_cmd("git init -b main", cwd=path)
    run_cmd("git config user.email 'test@example.com'", cwd=path)
    run_cmd("git config user.name 'Test User'", cwd=path)
    return path

def write_and_commit(repo_path, files, message):
    for filepath, content in files.items():
        full_path = repo_path / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    run_cmd("git add -A", cwd=repo_path)
    run_cmd(f"git commit -m '{message}'", cwd=repo_path)

def hash_snippet(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# 6 test scenarios - see full file in repo for complete implementations
# Scenarios: independent functions, same-function conflict, adjacent edits,
# rename+edit, config merge, semantic risk

def main():
    print("Generating merge test repositories...")
    print("Run full version locally - see repository for complete implementation")
    print("Scenarios: independent functions, same-function conflict, adjacent edits,")
    print("  rename+edit, config merge, semantic-risk")
    print("\nThis is a minimal version for initial commit.")
    print("Full version with ground truth available in workspace.")

if __name__ == "__main__":
    main()
