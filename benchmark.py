#!/usr/bin/env python3
"""
Merge correctness benchmark
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

TEST_REPOS = Path("test-repos")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result

def test_merge(repo_path):
    """Test git merge on a repo"""
    # Reset to ours branch
    run_cmd("git checkout ours", cwd=repo_path)
    run_cmd("git reset --hard ours", cwd=repo_path)
    
    start = time.perf_counter()
    result = run_cmd("git merge theirs --no-commit --no-ff", cwd=repo_path)
    elapsed = (time.perf_counter() - start) * 1000
    
    # Check for conflicts
    status = run_cmd("git status --porcelain", cwd=repo_path)
    has_conflicts = "UU" in status.stdout
    
    # Count conflict markers
    conflict_count = 0
    for f in repo_path.rglob("*.py"):
        if f.is_file():
            content = f.read_text(errors='ignore')
            conflict_count += content.count("<<<<<<<")
    
    # Cleanup
    run_cmd("git merge --abort", cwd=repo_path)
    
    return {
        "time_ms": round(elapsed, 2),
        "has_conflicts": has_conflicts,
        "conflict_markers": conflict_count,
        "success": result.returncode == 0
    }

def main():
    print("Merge Correctness Benchmark")
    print("=" * 50)
    
    if not TEST_REPOS.exists():
        print("ERROR: Run generate_repos.py first")
        return
    
    scenarios = sorted([d for d in TEST_REPOS.iterdir() if d.is_dir()])
    print(f"\nTesting {len(scenarios)} scenarios\n")
    
    results = []
    for scenario in scenarios:
        print(f"Testing {scenario.name}...")
        result = test_merge(scenario)
        result["scenario"] = scenario.name
        results.append(result)
        status = "CONFLICT" if result["has_conflicts"] else "CLEAN"
        print(f"  Result: {status}, Time: {result['time_ms']}ms")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "git_version": run_cmd("git --version").stdout.strip(),
        "results": results
    }
    
    results_file = RESULTS_DIR / "results.json"
    with open(results_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Generate RESULTS.md
    with open("RESULTS.md", "w") as f:
        f.write("# Merge Benchmark Results\n\n")
        f.write(f"Generated: {output['timestamp']}\n\n")
        f.write(f"Git: {output['git_version']}\n\n")
        f.write("| Scenario | Time (ms) | Conflicts | Markers |\n")
        f.write("|----------|-----------|-----------|----------|\n")
        for r in results:
            f.write(f"| {r['scenario']} | {r['time_ms']} | {r['has_conflicts']} | {r['conflict_markers']} |\n")
    
    print(f"\nResults saved to {results_file}")

if __name__ == "__main__":
    main()
