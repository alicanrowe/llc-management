#!/usr/bin/env python3
"""Read entity.md and say what needs attention, before you tell the owner any deadline or status.

  python3 scripts/deadlines.py entity.md [--today 2026-11-18] [--soon 60]

Flags (exit code 1 if any):
  STALE RECORD   the state record was last checked more than 30 days ago (or never): check it before stating a deadline
  OVERDUE        a deadline whose date has passed and whose status isn't done
  DUE SOON       a deadline inside --soon days that isn't done
  NO REMINDER    a deadline inside --soon days with no reminder listed under "Reminders set"
  RENEWS         a provider set to auto-renew within 30 days (cancel or keep, on purpose)
  AGENT LOCK     a registered agent service set to auto-renew within 120 days: providers won't cancel while they are on the
                 state record, so a state change filing must be processed first (file 8+ weeks before the renewal)
Standard library only. entity.md holds private details: never print it whole into a chat or a public file."""
import argparse, re, sys
from datetime import date, timedelta


def table(md, heading):
    m = re.search(r"^## " + re.escape(heading) + r".*?\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    if not m: return []
    rows = [l.strip().strip("|").split("|") for l in m.group(1).splitlines() if l.strip().startswith("|")]
    if len(rows) < 2: return []
    head = [h.strip().lower() for h in rows[0]]
    return [dict(zip(head, [c.strip() for c in r])) for r in rows[2:] if any(c.strip() for c in r)]


def d(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    return date(*map(int, m.groups())) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entity"); ap.add_argument("--today"); ap.add_argument("--soon", type=int, default=60)
    a = ap.parse_args()
    md = open(a.entity).read(); today = d(a.today) if a.today else date.today()
    flags = []
    chk = re.search(r"## State record \(last checked: ([^)]*)\)", md)
    last = d(chk.group(1)) if chk else None
    if not last or (today - last).days > 30:
        flags.append(f"STALE RECORD: state record last checked {last or 'never'}; check the state's entity search before stating any deadline")
    rem = re.search(r"Reminders set:(.*)", md); rem = (rem.group(1) if rem else "").lower()
    for r in table(md, "Deadlines"):
        when = d(r.get("date")); what = r.get("what", "?"); st = r.get("status", "").lower()
        if not when or st.startswith("done"): continue
        if when < today: flags.append(f"OVERDUE: {what} was due {when} (status: {st or 'blank'})")
        elif when - today <= timedelta(days=a.soon):
            flags.append(f"DUE SOON: {what} on {when} ({(when - today).days} days)")
            if what.lower()[:12] not in rem and str(when) not in rem:
                flags.append(f"NO REMINDER: {what} on {when} has no reminder listed under 'Reminders set'")
    for r in table(md, "Providers"):
        pt = d(r.get("paid through")); ar = r.get("auto-renew", "").lower()
        svc = (r.get("service", "") or "").lower()
        if pt and ar.startswith("y") and "agent" in svc and 0 <= (pt - today).days <= 120:
            flags.append(f"AGENT LOCK: {r.get('provider', '?')} {r.get('service', '')} auto-renews {pt}; file the state change (new agent or revoke) and send the receipt to the provider before then")
        if pt and ar.startswith("y") and 0 <= (pt - today).days <= 30:
            flags.append(f"RENEWS: {r.get('provider', '?')} {r.get('service', '')} auto-renews {pt}; cancel or keep it on purpose")
    print("\n".join(flags) if flags else "nothing due; state record is fresh")
    sys.exit(1 if flags else 0)


if __name__ == "__main__":
    main()
