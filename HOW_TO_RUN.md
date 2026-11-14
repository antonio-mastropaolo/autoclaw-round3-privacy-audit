# HOW TO RUN THIS AUDIT (operator steps)

AutoClaw is a GUI app, so **you start the run**. Everything else is prepared.

---

## 1. Open

AutoClaw → **Legal Assistant** (GLM-5.3-FlashX-Legal).

## 2. Attach

Exactly the two files in `upload/`, nothing else:

```
upload/00_MATTER_BRIEF.md
upload/JOPLIN_PRIVACY_POLICY.md
```

`PRIVATE_KEY/GROUND_TRUTH.md` is the answer key. It is published so a reader can verify the
score, but the agent must not see it or the run measures nothing.

## 3. Point it at the code

The audit needs the source, which is far too large to paste. Give AutoClaw the clone:

```
/tmp/jop
```

To re-clone at the exact pin instead:

```
git clone --depth 1 --filter=blob:none --sparse https://github.com/laurent22/joplin.git
cd jop && git sparse-checkout set packages/lib packages/app-desktop packages/app-mobile packages/app-cli
git checkout f1b8a6351cdced9a9525b2c4bbe121d4b6c0dc28
```

## 4. Ask for

The brief already fixes the deliverable table and the allowed verdict/severity words. Add only
this, verbatim:

> Cite every finding as `file:line` and quote the line. Do not report a host as a live call
> unless you can show the call site. If you cannot settle a claim from the code in scope, mark it
> UNVERIFIABLE rather than guessing.


---

## 5. After the run

1. Save the agent's raw output as `RESULT_agent_raw.md`.
2. Score it against `PRIVATE_KEY/GROUND_TRUTH.md` (12 items, −1 per false positive).
3. Write the human verification pass into `verification_lessons.md` — what the agent got right,
   what it got wrong, and any place the KEY itself was wrong (that is a legitimate outcome and
   must be recorded, not hidden).
4. Only then publish the post.

> This is how the Round 3 kit went wrong the first time: corrections were written down but never
> applied to the artifacts. Do not repeat that — fix the artifacts in the same pass.
