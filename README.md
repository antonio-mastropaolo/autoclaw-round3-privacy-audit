# Privacy Policy vs. Code Reality — a Joplin audit

**An AutoClaw Round 3 entry (Legal Practice).** A published privacy policy says 11 specific
things about what an app connects to. The code says something slightly different. This kit is the
audit that finds out where, with a `file:line` for every claim.

> **Not legal advice.** A software-engineering audit in counsel's clothes. Joplin is a real
> open-source project; the "counsel memo" framing is the exercise's shape, not an opinion about
> Joplin's legal position.

---

## Why this use case beats the last one

The Round 3 kit I first built asked a CS professor to play lawyer over a fictional contract. Two
weaknesses, both real:

1. **The score was self-graded.** It rested on a private 20-issue answer key *I wrote*, applied to
   a contract *I also wrote*. A judge had to take the 19.5/20 on faith.
2. **Domain credibility.** A professor publishing a "counsel memo" invites the obvious jeer.

Here the ground truth is **the source code of a real public project**. Somebody can: clone the
repo at the pinned commit, run the same audit, and check every row of the score independently.
The score is reproducible, not asserted. And the auditor is a computer scientist auditing code,
which is the right person for the job.

---

## Files

| File | What it is |
|---|---|
| `README.md` | This overview. |
| `matter/00_MATTER_BRIEF.md` | The task: 11 policy claims + the deliverable table + allowed verdict vocabulary. |
| `matter/JOPLIN_PRIVACY_POLICY.md` | The real policy under test, verbatim, at the pinned commit. |
| `PRIVATE_KEY/GROUND_TRUTH.md` | Hand-verified answer key, **published on purpose** so you can check the score yourself. The agent never sees it: it is given the Joplin clone and the two files in `upload/`, and nothing else. |
| `HOW_TO_RUN.md` | Operator steps: what to attach, what to point AutoClaw at, how to score. |
| `upload/` | Exactly the two files the agent sees. |

---

## Status

- [x] Matter prepared against `laurent22/joplin@f1b8a63`
- [x] Ground-truth key written from a hand audit of the same commit
- [x] Upload set isolated from the key
- [ ] AutoClaw run — **operator starts this** (GUI app)
- [ ] Scoring pass
- [ ] X post
