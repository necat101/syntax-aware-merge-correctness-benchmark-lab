# Verification Transcript

## Fresh Clone Verification
**Date**: 2026-06-25 20:22 UTC  
**Repository**: https://github.com/necat101/syntax-aware-merge-correctness-benchmark-lab  
**Commit**: cebfa12d15eb426363f4989c6a4bf23a6f85c73c

### Clone and Verify
```bash
$ git clone https://github.com/necat101/syntax-aware-merge-correctness-benchmark-lab.git
Cloning into 'syntax-aware-merge-correctness-benchmark-lab'...
remote: Enumerating objects: 18, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 18 (delta 2), reused 18 (delta 2), pack-reused 0
Receiving objects: 100% (18/18), done.

$ cd syntax-aware-merge-correctness-benchmark-lab
$ ls -la
total 28
drwxr-xr-x  4 user user 4096 Jun 25 20:24 .
drwxr-xr-x  3 user user 4096 Jun 25 20:24 ..
drwxr-xr-x  8 user user 4096 Jun 25 20:24 .git
-rw-r--r--  1 user user  5188 Jun 25 20:24 README.md
-rw-r--r--  1 user user  1312 Jun 25 20:24 RESULTS.md
-rw-r--r--  1 user user  2460 Jun 25 20:24 VERIFY.md
-rw-r--r--  1 user user  2919 Jun 25 20:24 benchmark.py
-rw-r--r--  1 user user  4557 Jun 25 20:24 generate_repos.py

$ python3 -m py_compile generate_repos.py benchmark.py
$ echo $?
0
✓ Both files compile successfully

$ python3 generate_repos.py
Generating test repositories...
✓ 01-different-functions
✓ 02-same-function
✓ 03-adjacent-edits

Generated 3/3 scenarios
Output: test-repos

$ python3 benchmark.py
Merge Correctness Benchmark
==================================================

Testing 3 scenarios

Testing 01-different-functions...
  Result: CLEAN, Time: 67.63ms, Markers: 0
Testing 02-same-function...
  Result: CONFLICT, Time: 58.77ms, Markers: 1
Testing 03-adjacent-edits...
  Result: CONFLICT, Time: 57.88ms, Markers: 1

Results saved to results/results.json
Summary written to RESULTS.md

$ cat RESULTS.md | grep -A 5 "## Results"
## Results

| Scenario | Time (ms) | Conflicts | Markers |
|----------|-----------|-----------|----------|
| 01-different-functions | 67.63 | False | 0 |
| 02-same-function | 58.77 | True | 1 |
| 03-adjacent-edits | 57.88 | True | 1 |
```

### Verification Summary
- ✅ Repository clones successfully
- ✅ All Python files pass py_compile (exit code 0)
- ✅ Generator creates 3 test scenarios with git histories
- ✅ Benchmark executes and produces results
- ✅ RESULTS.md generated with real benchmark data
- ✅ No external dependencies required (uses only stdlib + git)

### File Integrity
```
generate_repos.py: 4,557 bytes - Creates test git repos with scenarios
benchmark.py: 2,919 bytes - Runs merges and measures results
README.md: 5,188 bytes - Documentation
RESULTS.md: 1,312 bytes - Real benchmark results
VERIFY.md: 2,460 bytes - This verification transcript
```

### Test Execution Details
- **Python version**: 3.12.3
- **Git version**: git version 2.43.0
- **Platform**: Linux 6.17.0-1009-aws x86_64
- **Test scenarios**: 3 (different-functions, same-function, adjacent-edits)
- **Strategies tested**: 1 (git-merge only - mergiraf/weave not installed)

### Limitations Noted
- Only basic git merge tested (mergiraf/weave not available in test environment)
- Single trial per scenario (not 3x as specified in requirements)
- No validation of merged content correctness (only conflict detection)
- No compile/parsing validation of results
- Limited to 3 scenarios (not full set described in requirements)

**Verified**: Scripts execute end-to-end from fresh clone and produce auditable results
