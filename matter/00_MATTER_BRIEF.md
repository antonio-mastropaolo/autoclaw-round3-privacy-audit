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
