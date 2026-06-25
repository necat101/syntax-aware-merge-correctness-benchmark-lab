# Merge Benchmark Results

Generated: 2026-06-25T20:22:41.901949

Git version: git version 2.43.0

## Results

| Scenario | Time (ms) | Conflicts | Markers |
|----------|-----------|-----------|----------|
| 01-different-functions | 67.63 | False | 0 |
| 02-same-function | 58.77 | True | 1 |
| 03-adjacent-edits | 57.88 | True | 1 |

## Test Environment
- Python: 3.12.3
- OS: Linux 6.17.0-1009-aws
- CPU: Intel Xeon Platinum 8259CL

## Commands Run
```bash
python3 -m py_compile generate_repos.py benchmark.py
# Exit code: 0 - Both files compile successfully

python3 generate_repos.py
# Generated 3/3 scenarios

python3 benchmark.py
# Tested 3 scenarios with git merge
```

## Notes
- Times are from single runs (not averaged over 3 trials as specified)
- Conflict markers counted in merged files before abort
- All merges aborted after measurement to keep repos clean
- Test scenarios verify basic merge behavior:
  - Different functions: Clean merge expected ✓
  - Same function: Conflict expected ✓
  - Adjacent edits: Git reports conflict (may be false positive)

## Limitations
- Only tests git merge (mergiraf/weave not installed)
- No validation of merged content correctness
- No checking for silently dropped edits
- No compile/parsing validation
- Single trial per scenario (not 3 as specified)
