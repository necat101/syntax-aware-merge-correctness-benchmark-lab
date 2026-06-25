#!/usr/bin/env python3
"""
Generate reproducible synthetic git histories for merge testing.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("test-repos")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result

def init_repo(path):
    path.mkdir(parents=True, exist_ok=True)
    run_cmd("git init", cwd=path)
    run_cmd("git config user.email 'test@example.com'", cwd=path)
    run_cmd("git config user.name 'Test'", cwd=path)
    return path

def main():
    print("Generating test repositories...")
    # Simplified version - creates basic test structure
    # Full implementation would create the 4 scenarios described in README
    
    # Create a simple test repo
    repo = init_repo(OUTPUT_DIR / "test-scenario")
    
    # Base commit
    (repo / "test.py").write_text("def foo():\n    pass\n")
    run_cmd("git add -A", cwd=repo)
    run_cmd("git commit -m 'Initial'", cwd=repo)
    
    print("Test repos generated in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
