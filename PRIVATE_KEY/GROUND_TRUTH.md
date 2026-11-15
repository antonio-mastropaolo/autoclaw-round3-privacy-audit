# GROUND-TRUTH KEY — do NOT upload this to the agent

Hand audit of `laurent22/joplin@f1b8a6351cdced9a9525b2c4bbe121d4b6c0dc28`, scope
`packages/{lib,app-desktop,app-mobile,app-cli}` (tests, `locales/`, `*.d.ts` excluded), written
before the AutoClaw run. This file is published so a reader can check the score; the agent is
given the Joplin clone and the two files in `upload/`, and nothing else.

Every row is a **decision**: the verdict an honest audit must reach, the evidence that settles it,
and what earns credit. Epistemic tags:

- **PROVEN** — read at the cited `file:line` in the pinned commit.
- **INFERRED** — depends on a library outside the audit scope (Electron, tesseract.js, NetInfo,
  the Sentry SDK). An agent cannot prove these from the code in scope either, so UNVERIFIABLE is an
  accepted verdict wherever the host itself lives only inside such a library.

All `builtInMetadata.ts` paths below are `packages/lib/models/settings/builtInMetadata.ts`.

---

## Decision table — 11 policy rows + 2 undisclosed hosts (13 scored rows)

| Row | Policy claim | Correct verdict | Accepted severity | Evidence |
|---|---|---|---|---|
| R1 | Auto-update → `objects.joplinusercontent.com`, Enabled, can disable | **CONSISTENT** | — | PROVEN. `packages/app-desktop/checkForUpdates.ts:28` `shim.fetch('https://objects.joplinusercontent.com/r/releases')`; gated by `packages/app-desktop/app.ts:663` `if (Setting.value('autoUpdateEnabled'))`; default `builtInMetadata.ts:1868` `value: true`. Runs only on Windows/macOS (`app.ts:661`), which is why the setting is hidden on Linux (`public: platform !== 'linux'`). |
| R2 | Geo-location → `ipwho.is` **or** `geoplugin.net`, Enabled | **OVERSTATED** | P1 (P2 accepted) | PROVEN. `packages/lib/geolocation-node.ts:30` `fetchJson('https://ipwho.is/')`; the `geoipServices` map (`:27-43`) has one key, `ipwhois`. `geoplugin.net` appears nowhere in product code, only inside the embedded copy of the policy text at `packages/lib/welcomeAssets.js:57`. Default `builtInMetadata.ts:1330` `value: true` matches. |
| R3 | Synchronisation → third party, Disabled | **CONSISTENT** | — | PROVEN. `builtInMetadata.ts:152-153` `'sync.target': { value: 0` (no target). |
| R4 | Wifi connection check (mobile), Enabled, cannot disable, **no host named** | **UNDERSTATED** | P1 or P2 | PROVEN that the host is configured: `packages/app-mobile/root.tsx:428` `reachabilityUrl: 'https://joplinapp.org/connection_check/'`, set unconditionally at startup (not gated on `sync.mobileWifiOnly`). The policy names no host for this row. INFERRED: whether NetInfo fetches that URL on a given platform depends on the NetInfo library's native-reachability path. |
| R5 | Spellchecker dictionary → `redirector.gvt1.com` (Linux/Windows), Enabled, can disable | **CONSISTENT** or **UNVERIFIABLE** | — | `redirector.gvt1.com` is **not in Joplin's code**. PROVEN: Joplin only calls Electron's `session.setSpellCheckerLanguages` / `setSpellCheckerEnabled(effectiveLanguages.length > 0)` (`packages/app-desktop/services/spellChecker/SpellCheckerServiceDriverNative.ts:62-63`) and never overrides the download URL. INFERRED: the host is Chromium's default dictionary server. |
| R6 | Plugin repository → GitHub + mirrors, Enabled, cannot disable | **CONSISTENT** | — (mirror nuance P2 accepted) | PROVEN. `packages/lib/services/plugins/RepositoryApi.ts:92` `https://github.com/joplin/plugins`; mirror list `:35-41`: `cdn.staticaly.com`, `ghproxy.com`, `cdn.jsdelivr.net`, `raw.fastgit.org`. The policy discloses the mirrors only by a link to an older commit's list. Flagging that as a P2 wording gap is fair, not a false positive. |
| R7 | Voice typing → `github.com/joplin/voice-typing-models` **or** `alphacephei.com`, Disabled | **OVERSTATED** | P1 (P2 accepted) | PROVEN. The only model source is `packages/app-mobile/services/voiceTyping/whisper.ts:222` `'https://github.com/joplin/voice-typing-models/releases/download/v0.2.0/{task}.zip'` (user-overridable via `voiceTypingBaseUrl`). Vosk, the `alphacephei.com` engine, is marked `'vosk': 'Vosk', // No longer supported` at `builtInMetadata.ts:2554`; `alphacephei` appears nowhere in product code. Same defect class as R2: the policy names a host the code no longer contacts. |
| R8 | OCR → `cdn.jsdelivr.net/npm/@tesseract.js-data/`, Enabled, can disable | **CONSISTENT** or **UNVERIFIABLE** | — | Default PROVEN: `builtInMetadata.ts:590-591` `'ocr.enabled': { value: true`. The host is **not in Joplin's code**: `packages/app-desktop/app.ts:417` passes `Setting.value('ocr.languageDataPath') \|\| null`, and `packages/lib/services/ocr/drivers/OcrDriverTesseract.ts:121` sets `langPath` only when that is non-empty. INFERRED: with no `langPath`, tesseract.js falls back to its own jsDelivr default. **Wrong cite trap:** `cdn.jsdelivr.net` at `RepositoryApi.ts:39` is a *plugin mirror*, not OCR. Citing it for OCR scores 0.5. |
| R9 | Crash reports → Sentry, "upload the report", Disabled | **UNDERSTATED** | P0 or P1 | PROVEN. `packages/app-desktop/bridge.ts:103` `Math.min(size, 100 * KB)`, `:119` `{ filename: 'joplin-log.txt', data: lines }`, `:126` `hint.attachments = [logAttachment]`: up to 100 KB of the local log tail is attached to the event. INFERRED: that the Sentry SDK transmits `hint.attachments` set in `beforeSend` (standard SDK behaviour, but the SDK is outside scope). Default `builtInMetadata.ts:1871-1872` `value: false` matches the policy. **Nuance (full credit only if stated precisely):** `Sentry.init(options)` runs always (`bridge.ts:65` → `:165`), but the DSN is set only when the flag is on (`:160`) and `beforeSend` returns `null` when it is off (`:147`). With crash upload disabled nothing is sent. A local crash dump containing the log is still written to disk (`:141`), which is local and not a policy breach. |
| R10 | Handwriting recognition → Joplin Server/Cloud, Disabled | **CONSISTENT** | — | PROVEN. Default `builtInMetadata.ts:617-618` `value: false`; transport `packages/lib/services/ocr/drivers/OcrDriverTranscribe.ts:73` `api.exec('POST', 'api/transcribe', …)` through the configured sync target's API. |
| R11 | Beta feedback (web app) → `objects.joplinusercontent.com`, Enabled | **OVERSTATED** | P2 (P1 accepted) | PROVEN absence. The only related code is `builtInMetadata.ts:2502-2504`, `'survey.webClientEval2025.progress'` with `// Ended in February 2026`, default `SurveyProgress.Dismissed`, and nothing else in scope reads it. No feedback call site to `objects.joplinusercontent.com` exists: that host's only call sites are the two update checks (`checkForUpdates.ts:28`, `services/autoUpdater/AutoUpdaterService.ts:21`). The policy row describes a feature that is gone, so there is no data-flow consequence. |
| U1 | *(no policy row)* `api.ipify.org` | **UNDISCLOSED** | P2 (P1 accepted) | PROVEN. `packages/lib/net-utils.ts:4` `shim.fetch('https://api.ipify.org/?format=json')` inside `export async function ip()`. **`ip()` has no caller in scope**: every importer of `net-utils` takes only `getHttpStatusMessage`, `findAvailablePort` or `mimeTypeFromHeaders` (`JoplinServerApi.ts:8`, `onedrive-api-node-utils.ts:2`, `services/rest/routes/notes.ts:25`, `app-cli/app/ResourceServer.ts:2`). So it is dead code here. An agent that says so earns full credit at P2; P1 without the reachability note also earns full credit. |
| U2 | *(no policy row)* AI providers (`api.anthropic.com`, user-supplied OpenAI-compatible URL) | **UNDISCLOSED** | P2 | PROVEN. `packages/lib/services/ai/providers/Anthropic.ts:229` `shim.fetch('https://api.anthropic.com/v1/messages', …)`; opt-in at every layer: `builtInMetadata.ts:667-668` `'ai.enabled': { value: false`, `:689-690` `'ai.allowRemote': { value: false`, `:740-741` `'ai.chat.baseUrl': { value: ''`. `api.openai.com` occurs only in a setting's help text (`builtInMetadata.ts:748`). The policy never mentions AI, which is a P2 omission. |

### Not scored (credit-neutral)

- **U3 — `api.github.com` on Android.** `packages/app-mobile/components/ScreenHeader/WarningBanner.tsx:49`
  fetches `https://api.github.com/repos/laurent22/joplin-android/releases/tags/android-v…`, only when
  the sync target demands a newer app (`:62`). It is a real, conditional, undisclosed call. Finding it
  is a sign of a thorough audit, but it is not in the denominator; reporting it as UNDISCLOSED/P2 is
  never a false positive.

---

## False-positive traps (−1.0 each)

| Trap | Why it is wrong |
|---|---|
| T1 — R1/R3/R10 flagged as defects | The auto-update host, sync default and handwriting default match the code exactly. |
| T2 — AI providers called a silent / automatic phone-home | Off by default and remote-blocked by default (`ai.enabled`, `ai.allowRemote` both `false`). |
| T3 — "Joplin calls `geoplugin.net`" | Its only occurrence is the policy text embedded in `welcomeAssets.js:57`, which is not a call site. |
| T4 — "Sentry sends data when crash upload is disabled" | No DSN (`bridge.ts:160`) and `beforeSend` returns `null` (`:147`). |
| T5 — "`api.ipify.org` is called on startup / on every note" | `ip()` has no caller in scope. |

---

## Scoring (fixed denominator = 13)

Per row: **1.0** correct verdict (any listed alternative), a correct `file:line` for the deciding
evidence, and a usable fix · **0.5** correct verdict but wrong or missing cite (including the R8
plugin-mirror cite) · **0** wrong verdict or missed.
Severity outside the accepted set: −0.25 on that row.
**Subtract 1.0 per false positive** (traps above, or any defect the code disproves). Floor at 0.

A high score with a false positive is worse than a slightly lower score without one; say so in the
write-up. Maximum = 13.0.

Mechanical pre-check: `python3 tools/score_run.py RESULT_agent_raw.md` flags which rows have the
evidence markers present. The final grade is human: a marker can sit inside a wrong claim.

---

## Revision log (kept on purpose)

The first version of this key (commit `178c791`) was re-checked line by line against the pinned
clone on 2026-11-14, **before** any agent run, and was wrong in ways that would have mis-scored a
correct agent:

1. **It called `alphacephei.com` "real".** It is not in product code; Vosk is "No longer supported".
   The old key would have charged a −1 false positive to an agent that correctly reported R7 as
   OVERSTATED.
2. **It called `redirector.gvt1.com` "1 file, real".** Zero occurrences. The host is Electron's
   default, not Joplin's code.
3. **It credited `cdn.jsdelivr.net` to OCR ("2 files").** One occurrence, and it is a plugin mirror.
4. **It treated `api.ipify.org` as a live P1 call.** `ip()` has no caller in scope.
5. **It missed R4** (`joplinapp.org/connection_check`) **and R11** (the beta-feedback feature is gone).
6. **Two line numbers were off by one or two:** `joplin-log.txt` is at `bridge.ts:119` (not 118),
   and `Sentry.init` is at `:165` (not 163).
7. **Six of the eleven policy rows had no evidence at all.** They would have been graded from memory
   at scoring time, which is the self-grading problem this kit exists to avoid.
