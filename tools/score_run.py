#!/usr/bin/env python3
"""score_run.py -- mechanical pre-check of an AutoClaw output against the ground-truth key.

This does NOT assign the final score. It answers one narrow question per ground-truth item:
did the output contain the specific evidence marker that item requires? Final scoring is human
(a marker can be present in a wrong claim). But it makes the pass reproducible and stops the
most common failure: scoring from memory of what the agent ""seemed"" to say.

Usage: python3 tools/score_run.py RESULT_agent_raw.md
"""
import json, re, sys, pathlib

ITEMS = [
    ("K1", "geolocation names ipwho.is AND geoplugin.net; only ipwhois implemented",
     [r"geolocation-node\.ts", r"ipwho\.is"], [r"geoplugin"]),
    ("K2", "crash report attaches up to 100KB of log",
     [r"bridge\.ts"], [r"100\s*\*?\s*KB|100KB|joplin-log"]),
    ("K3", "api.ipify.org is an undisclosed call",
     [r"ipify"], [r"net-utils\.ts"]),
    ("K4", "Sentry.init runs regardless of the DSN/upload flag",
     [r"[Ss]entry"], [r"init"]),
    ("F1", "FALSE-POSITIVE TRAP: disclosed hosts are correct, not defects",
     [], [r"objects\.joplinusercontent", r"redirector\.gvt1"]),
    ("F2", "FALSE-POSITIVE TRAP: AI providers are user-configured, not phone-home",
     [], [r"api\.anthropic|api\.openai|mistral"]),
]

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    txt = pathlib.Path(sys.argv[1]).read_text(errors="ignore")
    low = txt.lower()
    print(f"scoring {sys.argv[1]}  ({len(txt)} chars)\n")
    for key, desc, cites, markers in ITEMS:
        hit_cite = all(re.search(c, txt, re.I) for c in cites) if cites else True
        hit_mark = any(re.search(m, txt, re.I) for m in markers) if markers else True
        status = "EVIDENCE PRESENT" if (hit_cite and hit_mark) else "MISSING EVIDENCE"
        print(f"  {key}  {status:20s}  {desc}")
    print("\nReminder: presence of a marker is not proof of a correct claim. Read the row.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
