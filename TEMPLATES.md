# Templates

Copy these. Fill them by hand. The friction is the point — typing it out is what encodes it.

---

## A. Daily log — `logs/YYYY-MM-DD.md`

```markdown
# 2026-08-03  ·  Day 1 / Week 1

## B1 — Recall (25 min)
| Problem | Pattern recalled? | Insight in 1 line | Next interval |
|---|---|---|---|
|  |  |  |  |

## A — New problems (90 min)

### Problem 1: <name>  [medium/hard]
- **Clarifying questions I asked:**
- **Brute force + complexity:**
- **Bottleneck (one sentence):** "It's O(...) because I recompute ___ for every ___."
- **Optimization + complexity:**
- **Invariant I wrote before coding:**
- **Time taken vs. budget:** __ / 35 min
- **Outcome:** SOLVED_CLEAN / SOLVED_WITH_HINT / SOLVED_BY_READING / FAILED
- **Failure class(es):**
- **Key insight (must fit one line — this is what you'll review):**

### Problem 2: <name>
(same)

## C — GPU (60 min)
- Studied:
- Wrote / measured:
- Number that surprised me:
- Question I couldn't answer:

## D — Python (45 min)
- Topic:
- Thing I didn't know before today:

## B2 — Retro (5 min)
- Dominant failure class today:
- Energy 1–5:
- Tomorrow's first problem (decide now):
```

---

## B. Review tracker — `logs/review.md`

One row per solved problem. Sort by `Next Review` each morning.

```markdown
| # | Problem | Pattern | One-line insight | Solved | Streak | Next Review |
|---|---------|---------|------------------|--------|--------|-------------|
| 1 |         |         |                  | 08-03  | 0      | 08-04       |
```

**Intervals:** streak 0→+1d · 1→+3d · 2→+7d · 3→+21d · 4→+60d
**Fail a rep → streak resets to 0.**

A rep passes only if, within 90 seconds and without notes, you can state: (1) the pattern, (2) the key insight, (3) time and space complexity. Not the code.

---

## C. Failure log — `logs/failures.md`

Append-only. Never delete a row. Review every Sunday.

```markdown
| Date | Problem | Class | What actually happened | What I'll check next time |
|------|---------|-------|------------------------|---------------------------|
```

**Classes:** `OFF_BY_ONE` `EMPTY_INPUT` `SINGLE_ELEMENT` `DUPLICATES` `OVERFLOW/PRECISION` `NEGATIVE_ZERO` `CYCLE_UNHANDLED` `MUTATION_DURING_ITERATION` `WRONG_INVARIANT` `PATTERN_NOT_RECOGNIZED` `COMPLEXITY_MISJUDGED` `PREMATURE_OPTIMIZATION`

---

## D. Pattern card — `patterns/<pattern>.md`

Write one per pattern, in your own words, only *after* you've solved 3+ problems with it. Writing it before is copying; writing it after is compression.

```markdown
# Monotonic Stack

## Trigger — what in the problem statement makes me reach for this?
(e.g. "next greater/smaller element", "largest rectangle", "span")

## The invariant
What is always true about the stack contents?

## Why it's O(n) despite the nested-looking loop
(amortized argument — each element pushed once, popped once)

## Skeleton I can reconstruct from memory
(pseudocode, not a copy-paste solution)

## Variants
- increasing vs. decreasing
- indices vs. values on the stack
- sentinel elements

## Problems I've solved with it
## Where I went wrong the first time
```

---

## E. Sunday retro — `logs/week-NN-retro.md`

```markdown
# Week NN Retro

## Numbers
- Problems attempted / solved clean / solved by reading:
- Reps due / reps passed:
- Days hit full 4h / minimum viable / missed:

## Failure class counts this week
| Class | Count |
|---|---|

## The one class I'm targeting next week:
## Three problems chosen specifically to trigger it:

## GPU: what I can now explain that I couldn't last Sunday
## Python: same

## What went wrong process-wise (not knowledge-wise)
## One change to the routine for next week (max one)

## Next week's daily plan
| Day | Problems | GPU topic | Python topic |
|---|---|---|---|
```

---

## F. Mock interview scorecard — from Week 5

```markdown
| Dimension | 1–5 | Note |
|---|---|---|
| Restated problem before solving | | |
| Asked clarifying questions unprompted | | |
| Stated brute force + complexity first | | |
| Explained bottleneck before optimizing | | |
| Talked continuously while coding | | |
| Dry-ran without being asked | | |
| Raised edge cases unprompted | | |
| Handled the follow-up question | | |
| Recovered gracefully when stuck | | |
```

Anything scoring ≤3 twice in a row becomes a deliberate drill, not a hope.
