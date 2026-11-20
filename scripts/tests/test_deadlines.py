"""python3 scripts/tests/test_deadlines.py : every planted problem in a fake entity.md is flagged."""
import os, subprocess, sys, tempfile
MD = """# Entity facts
## State record (last checked: 2026-09-01)
- Status: active
## Providers
| Provider | Service | Price | Paid through | Auto-renew | Status |
|---|---|---|---|---|---|
| ExampleCo | Registered agent | $119 | 2026-12-01 | yes | active |
| FarAgentCo | Registered agent | $199 | 2027-02-20 | yes | active |
| WebCo | Website | $15 | 2027-02-20 | yes | active |
## Deadlines
| Date | What | Basis | Fee | Status |
|---|---|---|---|---|
| 2026-10-01 | Publication affidavit | LLC Law 206 | $50 | to do |
| 2026-12-20 | Biennial statement | LLC Law 301 | $9 | to do |
| 2027-06-01 | Far away report | x | $0 | to do |
| 2026-11-01 | Old done thing | x | $0 | done |
## Links
- Reminders set: none
"""
p = os.path.join(tempfile.mkdtemp(), "entity.md"); open(p, "w").write(MD)
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deadlines.py"), p, "--today", "2026-11-18"],
                   capture_output=True, text=True)
want = ["STALE RECORD", "OVERDUE: Publication", "DUE SOON: Biennial", "NO REMINDER: Biennial", "RENEWS: ExampleCo", "AGENT LOCK: ExampleCo", "AGENT LOCK: FarAgentCo"]
miss = [w for w in want if w not in r.stdout]
extra = [w for w in ("Far away", "Old done", "WebCo", "RENEWS: FarAgentCo") if w in r.stdout]
print(r.stdout); print("deadlines ok" if r.returncode == 1 and not miss and not extra else f"FAIL missing {miss} extra {extra}")
sys.exit(0 if r.returncode == 1 and not miss and not extra else 1)
