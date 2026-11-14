# PRIVATE GROUND-TRUTH KEY — do NOT upload this to the agent

Written by hand from `laurent22/joplin@f1b8a63` before the AutoClaw run.
Every row below was verified by reading the cited source, not inferred.
This file lives in `PRIVATE_KEY/` and is excluded from the upload set.

---

## Verified true findings (the agent must find these)

### K1 — Geo-location names two providers; only one exists  [OVERSTATED / P1]
Policy: "For that it will connect to either `ipwho.is` or `geoplugin.net`."
Evidence: `packages/lib/geolocation-node.ts:30` implements ONLY ipwho.is:
  `const r = await fetchJson('https://ipwho.is/');`
and the `geoipServices` map has a single key, `ipwhois` (`geolocation-node.ts:27-42`).
`geoplugin.net` appears NOWHERE in product code — only inside the embedded copy of the policy
text at `packages/lib/welcomeAssets.js:57`. So the real and geoplugin fallbacks are not
implemented at this commit.

### K2 — Crash reports upload MORE than "the report"  [UNDERSTATED / P0]
Policy: "the application will upload the report to Sentry when a crash happens."
Evidence: `packages/app-desktop/bridge.ts:96-160`. The Sentry `beforeSend` hook attaches
the tail of the application log file:
  `const bytesToRead = Math.min(size, 100 * KB);`   (bridge.ts:103)
  `const logAttachment = { filename: 'joplin-log.txt', data: lines };`  (bridge.ts:118)
  `if (logAttachment) hint.attachments = [logAttachment];`      (bridge.ts:126)
So up to **100 KB of the local log** ships with every crash report, not just a stack trace.
That log can contain note titles, sync paths, hostnames, usernames. The policy says "the report",
which a reader will not read as "100 KB of my log". Default is Disabled (correct in policy), so
this is P0 only in the sense that it is the largest undisclosed data flow; severity P0 when the
user enables crash upload.

### K3 — `api.ipify.org`: an undisclosed outbound call  [UNDISCLOSED / P1]
Evidence: `packages/lib/net-utils.ts:4`:
  `const response = await shim.fetch('https://api.ipify.org/?format=json');`
This is a live call in the shipped lib, and `api.ipify.org` has NO row in the policy table.
The policy names only `ipwho.is`/`geoplugin.net` for IP geolocation. (Note the caller is a
utility `ip()` export; grade DOWN to P2 if the agent shows it is never reached from a product
entry point — that is a legitimate alternative read and should be scored as a correct nuance, not
as a miss.)

### K4 — Sentry DSN is hardcoded, so "Disabled" still initialises Sentry  [UNDERSTATED / P2]
Evidence: `bridge.ts:160` sets the DSN only when `autoUploadCrashDumps_` is true, but
`Sentry.init(options)` at `bridge.ts:163` runs ALWAYS ("sentryInit()" is called at
`bridge.ts:65`). With `beforeSend` returning null when the flag is off, no event is sent —
so no data leaves. The policy says "When Sentry is initialised it will also connect to
`sentry.io`" and calls default Disabled. That is CORRECT behaviour; the nuance is that
initialisation happens regardless. Score a finding here only if the agent states it precisely
(initialisation vs. transmission).

### K5 — Auto-update, spellcheck, OCR hosts are disclosed and real  [CONSISTENT]
  objects.joplinusercontent.com — 5 files, real
  redirector.gvt1.com            — 1 file, real
  cdn.jsdelivr.net               — 2 files, real
  alphacephei.com                — 1 file, real
These match the policy. An agent that flags them as problems has produced a FALSE POSITIVE.

### K6 — AI providers are user-configured, not silent phone-home  [CONSISTENT / P2 at most]
  `packages/lib/services/ai/providers/Anthropic.ts:229` — `https://api.anthropic.com/v1/messages`
  api.openai.com appears mostly in i18n example strings and provider config, api.mistral.ai likewise.
These fire only if the user configures an AI provider with a remote endpoint. NOT an undisclosed
automatic call. The policy does not mention AI providers at all — so at most a P2 omission.
An agent that calls this a "silent phone-home" is WRONG (false positive).

---

## Scoring (fixed denominator = 12)

The 12 scoreable items are: K1, K2, K3, K4, K5-consistency, K6-consistency, plus the six
policy rows an honest audit must confirm rather than invent (auto-update, wifi check, plugin repo,
voice typing, handwriting, beta feedback = 6 rows; K5/K6 fold in).

Score each: **1.0** found with a correct file:line cite and a usable fix · **0.5** found but
cite wrong, or right verdict with no evidence · **0** missed.
**Subtract 1.0 per FALSE POSITIVE** — a claimed defect the code disproves (see the K5/K6 traps).
Floor the total at 0.

A high score with a false positive is worse than a slightly lower score without one; say so in
the write-up. Maximum = 12.0.
