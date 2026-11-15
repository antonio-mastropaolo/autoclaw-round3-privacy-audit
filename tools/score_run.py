#!/usr/bin/env python3
"""score_run.py -- mechanical pre-check of an AutoClaw output against PRIVATE_KEY/GROUND_TRUTH.md.

It does NOT assign the final score. For each of the 13 scored rows it answers one narrow
question: does the output contain the evidence markers that row's decision rests on? For each
false-positive trap it reports whether the trap's tell appears, so a human reads that passage.
Final scoring is human, because a marker can sit inside a wrong claim. The point is to make the
pass reproducible and to stop scoring from memory of what the agent "seemed" to say.

Usage: python3 tools/score_run.py RESULT_agent_raw.md
"""
import re
import sys
import pathlib

# (row, expected verdict(s), description, required evidence markers -- ALL must match)
ROWS = [
    ("R1", "CONSISTENT", "auto-update host + gate",
     [r"checkForUpdates\.ts", r"objects\.joplinusercontent"]),
    ("R2", "OVERSTATED", "geoplugin.net named, only ipwho.is implemented",
     [r"geolocation-node\.ts", r"ipwho\.is", r"geoplugin"]),
    ("R3", "CONSISTENT", "sync target default 0",
     [r"sync\.target"]),
    ("R4", "UNDERSTATED", "wifi check pings joplinapp.org/connection_check",
     [r"root\.tsx", r"connection_check"]),
    ("R5", "CONSISTENT|UNVERIFIABLE", "spellchecker host is Electron's default",
     [r"[Ss]pell[Cc]hecker", r"redirector\.gvt1|setSpellChecker"]),
    ("R6", "CONSISTENT", "plugin repo + mirrors",
     [r"RepositoryApi\.ts"]),
    ("R7", "OVERSTATED", "alphacephei.com named, Vosk no longer supported",
     [r"whisper\.ts|voice-typing-models", r"[Vv]osk|alphacephei"]),
    ("R8", "CONSISTENT|UNVERIFIABLE", "OCR default on; host is tesseract.js default",
     [r"ocr\.enabled|OcrDriverTesseract|languageDataPath"]),
    ("R9", "UNDERSTATED", "crash report attaches up to 100 KB of log",
     [r"bridge\.ts", r"100\s*\*\s*KB|100\s*KB|joplin-log"]),
    ("R10", "CONSISTENT", "handwriting off by default, goes to Joplin Server",
     [r"handwritten|transcribe"]),
    ("R11", "OVERSTATED", "beta-feedback feature is gone",
     [r"[Ff]eedback|survey|webClientEval"]),
    ("U1", "UNDISCLOSED", "api.ipify.org call site, no caller in scope",
     [r"ipify", r"net-utils\.ts"]),
    ("U2", "UNDISCLOSED", "AI providers, opt-in",
     [r"api\.anthropic|Anthropic\.ts|ai\.enabled|allowRemote"]),
]

# (trap, tell regex -- if present, a human must read the passage)
TRAPS = [
    ("T1", "disclosed host/default flagged as a defect",
     r"(objects\.joplinusercontent|sync\.target|handwrit)[^\n]{0,200}\b(UNDERSTATED|UNDISCLOSED|P0)\b"),
    ("T2", "AI providers called a silent/automatic phone-home",
     r"(silent|automatic|phone[- ]home|without (the )?user)[^\n]{0,200}(anthropic|openai|mistral|\bAI\b)"
     r"|(anthropic|openai|mistral|\bAI\b)[^\n]{0,200}(silent|phone[- ]home|without (the )?user)"),
    ("T3", "claims geoplugin.net is actually called",
     r"welcomeAssets\.js[^\n]{0,200}(call|fetch|request)"),
    ("T4", "claims Sentry sends data when crash upload is disabled",
     r"(disabled|off)[^\n]{0,200}(still|nevertheless)[^\n]{0,80}(send|upload|transmit)"),
    ("T5", "claims ipify is called on startup / per note",
     r"ipify[^\n]{0,200}(startup|every note|each note|on launch)"),
]

R8_WRONG_CITE = r"RepositoryApi\.ts:39[^\n]{0,200}(OCR|tesseract)|(OCR|tesseract)[^\n]{0,200}RepositoryApi\.ts:39"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = pathlib.Path(sys.argv[1])
    txt = path.read_text(errors="ignore")
    print(f"pre-check of {path}  ({len(txt)} chars)\n")

    print("Scored rows (denominator 13):")
    present = 0
    for key, verdict, desc, markers in ROWS:
        ok = all(re.search(m, txt) for m in markers)
        verdict_seen = any(v in txt for v in verdict.split("|"))
        present += ok
        status = "EVIDENCE PRESENT" if ok else "MISSING EVIDENCE"
        vflag = "" if verdict_seen else f"  (verdict word {verdict} never appears)"
        print(f"  {key:4s} {status:17s} expect {verdict:24s} {desc}{vflag}")
    print(f"\n  markers present on {present}/13 rows (an upper bound, not a score)\n")

    print("False-positive traps (-1.0 each if the claim is really made):")
    for key, desc, tell in TRAPS:
        hit = re.search(tell, txt, re.I)
        status = "READ THIS PASSAGE" if hit else "no tell found"
        print(f"  {key}  {status:17s} {desc}")
        if hit:
            s = max(0, hit.start() - 80)
            print(f"        ...{txt[s:hit.end() + 80].replace(chr(10), ' ')}...")
    if re.search(R8_WRONG_CITE, txt, re.I):
        print("\n  R8 wrong-cite tell: RepositoryApi.ts:39 is the plugin mirror, not OCR -> 0.5 max on R8")

    print("\nReminder: a marker is not proof of a correct claim. Read every row against the key.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
