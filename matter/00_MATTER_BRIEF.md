# Matter Brief — Privacy Policy vs. Code Reality: Joplin

**A counsel-framed audit over a REAL open-source product.**
Audit target: `laurent22/joplin` at commit `f1b8a6351cdced9a9525b2c4bbe121d4b6c0dc28` (2026-11-14).

> **Not legal advice.** This is a software-engineering audit in counsel's clothes: the artifact under test is a published privacy policy, and the ground truth is the source code. Joplin is a real project; the "counsel memo" framing is the exercise's shape, not an opinion about Joplin's legal position.

---

## 1. The question

Joplin publishes a privacy policy at `readme/privacy.md`. Its opening claim is strong and falsifiable:

> "The Joplin applications ... do not send any data to any service without your authorisation."

It then lists **11 features** that do make network calls, each with a named host and a stated default:

| # | Feature | Named host | Stated default | Disableable |
|---|---|---|---|---|
| 1 | Auto-update | objects.joplinusercontent.com | Enabled | Yes |
| 2 | Geo-location | ipwho.is **or** geoplugin.net | Enabled | Yes |
| 3 | Synchronisation | third-party (OneDrive etc.) | Disabled | Yes |
| 4 | Wifi connection check | (mobile) | Enabled | No |
| 5 | Spellchecker dictionary | redirector.gvt1.com | Enabled | Yes |
| 6 | Plugin repository | GitHub / mirrors | Enabled | No |
| 7 | Voice typing | voice-typing-models, alphacephei.com | Disabled | Yes |
| 8 | OCR | cdn.jsdelivr.net | Enabled | Yes |
| 9 | Crash reports | sentry.io | Disabled | Yes |
| 10 | Handwriting recognition | Joplin Server/Cloud | Disabled | Yes |
| 11 | Beta feedback | objects.joplinusercontent.com | Enabled | Yes |

**The audit question:** for each of those 11 claims, is the code consistent with the policy? And, separately — does the code make network calls to hosts the policy never mentions?

---

## 2. Scope of the audit

Audit **only** these paths (the shipped product code, not the marketing site):

```
packages/lib/
packages/app-desktop/
packages/app-mobile/
packages/app-cli/
```

**Out of scope:** `readme/` (except as the policy under test), `locales/` translation strings, test files (`*.test.ts`, `*.spec.ts`), and any host appearing only inside a comment or an example URL.

**A host counts as a live call only if** it appears in a `fetch`/`fetchJson`/`shim.fetch`/`WebView`/`loadURL`/`axios`/`socket` call site, or in a settings default that enables one. Example URLs in docstrings and i18n strings are NOT calls.

---

## 3. Deliverable shape

Produce a **claim-by-claim table**, one row per policy claim plus one row per undisclosed host:

| Claim (policy sentence, quoted) | Policy code intent | Code evidence (file:line + quoted line) | Verdict | Severity | Fix |
|---|---|---|---|---|---|

Verdicts are only: **CONSISTENT** · **OVERSTATED** (code does less than policy says) · **UNDERSTATED** (code does more than policy says) · **UNDISCLOSED** (no policy row exists) · **UNVERIFIABLE** (cannot be settled from the code in scope).

Severity is only: **P0** (data leaves the device that the policy says does not) · **P1** (a stated default is wrong, or a named host is wrong) · **P2** (wording/omission, no data-flow change).
# HOW TO RUN THIS AUDIT (operator steps)

AutoClaw is a GUI app, so the run itself is **yours to start**. Everything else is prepared.

---

## 1. What to open

AutoClaw → **Legal Assistant** (GLM-5.3-FlashX-Legal), same mode as Round 3.

## 2. What to attach

**Attach the two files in `upload/`** and nothing else:

```
upload/00_MATTER_BRIEF.md
upload/JOPLIN_PRIVACY_POLICY.md
```

**Do NOT attach `PRIVATE_KEY/GROUND_TRUTH.md`.** It is the answer key. It lives in a
separate directory precisely so it cannot be dragged along by accident.

## 3. What to give it access to

The audit needs the **code**, which is far too large to paste. Point AutoClaw at the clone:

```
/tmp/jop
```

If it can be re-cloned instead, the exact pin is:

```
git clone --depth 1 --filter=blob:none --sparse https://github.com/laurent22/joplin.git
cd jop && git sparse-checkout set packages/lib packages/app-desktop packages/app-mobile packages/app-cli
git checkout f1b8a6351cdced9a9525b2c4bbe121d4b6c0dc28
```

## 4. What to ask for

The brief already specifies the deliverable table and the allowed verdict/severity vocabulary.
Add only this, verbatim:

> Cite every finding as `file:line` and quote the line. Do not report a host as a live call
> unless you can show the call site. If you cannot settle a claim from the code in scope, mark it
> UNVERIFIABLE rather than guessing.
