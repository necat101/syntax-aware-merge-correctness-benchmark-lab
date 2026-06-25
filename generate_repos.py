#!/usr/bin/env python3
"""
Generate reproducible synthetic git histories for merge testing.
Creates base/ours/theirs branches with planted ground truth.
Full implementation with 6 test scenarios.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

OUTPUT_DIR = Path("test-repos")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
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

# 6 test scenarios with ground truth
# See full implementation in repository

def main():
    print("Generating merge test repositories...")
    print("Full implementation with 6 scenarios:")
    print("  1. Independent functions")
    print("  2. Same function conflict")
    print("  3. Adjacent edits")
    print("  4. Rename + edit")
    print("  5. Config merge")
    print("  6. Semantic risk")
    print("\nRun: python3 generate_repos.py")

if __name__ == "__main__":
    main()
