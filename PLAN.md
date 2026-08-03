# 12-Week Plan — ML/GPU Interview Prep

**Target:** ML Systems / GPU / Inference roles (Anthropic, OpenAI, NVIDIA, Meta, Google)
**Start:** 2026-08-03 · **End:** 2026-10-25
**Budget:** 3h45 of work/day × 6 days (+15 min break) + 2h Sunday = **24.5h/week, ~294h total**
**Language:** Python (CUDA C++ read-level, Triton write-level)

---

## 0. The premise

You said "comfortable with mediums, hards are hit-or-miss." That diagnosis matters more than it sounds. Hards are rarely a knowledge gap — they're a **derivation gap**. You know what a monotonic stack is; you don't yet reliably *notice* that the problem in front of you wants one. So this plan spends less time on "learn the pattern" and more time on **recall under a clock** and **deriving the reduction**.

For the GPU roles specifically: these loops are usually **DSA + Python fluency + ML systems reasoning**, and increasingly a perf/kernel round. Kernels alone won't get you through; weak DSA will get you cut. Hence roughly 50/25/25.

### The four tracks

| Track | Weekly hours | What it buys you |
|---|---|---|
| **A. DSA under interview conditions** | 10h | The actual coding rounds |
| **B. Retention & edge-case discipline** | 3.5h | The difference between "solved once" and "can solve" |
| **C. GPU: architecture → CUDA → Triton** | 6h | The differentiator for ML/GPU roles |
| **D. Python depth + libraries** | 4.5h | Fluency that shows in every round |
| Sunday planning | 0.5h | Removes Monday-morning decision cost |

---

## 1. The daily 4 hours

Same shape every day. Don't redesign it each morning — decision fatigue is the #1 killer of consistency.

```
0:00 – 0:25   Block B1  Warm recall (spaced repetition, no IDE)
0:25 – 1:55   Block A   New problems, timed, interviewer protocol
1:55 – 2:10   ── break ──
2:10 – 3:10   Block C   GPU track
3:10 – 3:55   Block D   Python depth / concept study
3:55 – 4:00   Block B2  Log the day (5 min, non-negotiable)
```

### Block A protocol — treat every problem as a live interview

Set a timer. Speak out loud. This is the single highest-leverage habit in the plan.

| Phase | Medium | Hard | What you do |
|---|---|---|---|
| Clarify | 3 min | 5 min | Restate the problem in your own words. Ask 3 questions you'd ask an interviewer (input ranges? duplicates? empty? sorted? mutable?). Write 2 examples **by hand**, one of which is degenerate. |
| Brute force | 4 min | 7 min | State the dumb solution and its complexity. **Never skip this.** Interviewers award points for it, and it's where the optimization comes from. |
| Bottleneck | 3 min | 6 min | One sentence: "The brute force is O(n²) because I recompute X for every Y." The optimization is almost always a direct answer to that sentence. |
| Optimize | 5 min | 12 min | Propose, then state the new complexity *before* coding. |
| Code | 12 min | 20 min | No running it. Write it like a whiteboard. |
| Dry run | 5 min | 8 min | Trace your degenerate example by hand, line by line. |
| Edge cases | 3 min | 5 min | Write the list, then test. |
| **Total** | **35 min** | **63 min** | |

**Daily volume:** 2 mediums, or 1 hard + 1 medium. Quality over count — 2 problems fully processed beats 6 skimmed. Over 12 weeks that's ~144 problems, deeply.

**The 25-minute rule:** stuck 25 min past your budget → take a *hint*, not a solution. Read only the tags/topic. Stuck 10 more → read the first paragraph of an editorial, stop, and try again. Only read full solutions as a last resort, and if you do, that problem is marked `SOLVED_BY_READING` and re-attempted from scratch in 48h.

### Block B — retention (this is where most people leak progress)

**B1 (25 min, morning, no IDE):** pull 3–5 problems due for review. For each, you have **90 seconds** to state out loud: the pattern, the key insight in one sentence, and the complexity. If you can't → it resets to Day 1 of the interval.

Intervals: **1d → 3d → 7d → 21d → 60d.** Miss a rep, back to 1d.

Once per week, one of the "due" problems gets fully re-coded from scratch, not just recalled.

**B2 (5 min, evening):** the daily log. Every failure gets a **failure class**, not a description. Over 12 weeks this becomes the most valuable file you own — it tells you what *you specifically* get wrong.

Failure classes: `OFF_BY_ONE` · `EMPTY_INPUT` · `SINGLE_ELEMENT` · `DUPLICATES` · `OVERFLOW/PRECISION` · `NEGATIVE_ZERO` · `CYCLE_UNHANDLED` · `MUTATION_DURING_ITERATION` · `WRONG_INVARIANT` · `PATTERN_NOT_RECOGNIZED` · `COMPLEXITY_MISJUDGED` · `PREMATURE_OPTIMIZATION`

Weekly retro: whichever class appears most, you deliberately hunt problems that trigger it.

---

## 2. Edge-case engineering (your stated weak point)

Three mechanisms, added progressively:

**(a) The pre-code invariant statement — from Week 1.**
Before you write a loop, write one comment: *what is true at the top of every iteration?* Most off-by-ones are a violated invariant you never stated. Example, binary search: `# invariant: answer, if it exists, is within [lo, hi]`. That single line tells you whether the loop is `<` or `<=` and whether `hi = mid` or `mid - 1`.

**(b) The degenerate-input checklist — from Week 1.**
Before submitting, run mentally: empty · size 1 · size 2 · all identical · already sorted · reverse sorted · max constraint value · negative values · target absent · target at both ends.

**(c) Property-based testing with `hypothesis` — from Week 3.**
This is the trick almost nobody does, and it will change how you think. Write your optimized solution *and* the brute force, then let `hypothesis` generate thousands of random inputs and assert they agree. It will find your edge cases *for* you, and after a few weeks you start pre-empting them. Budget one Block D session per week for this.

---

## 3. Phases

### Phase 1 — Weeks 1–4: Rebuild the reflexes + GPU mental model

**Goal:** every core pattern recallable in <60s, and a correct mental model of *why GPUs are fast* before you write a single kernel.

| Week | Block A: DSA focus | Block C: GPU | Block D: Python |
|---|---|---|---|
| **1** | Arrays, hashing, two pointers, sliding window, prefix sums. Push to hard-tier variants. | Why memory is the bottleneck: cache hierarchy, latency numbers, bandwidth. Measure it yourself in NumPy. | Data model & dunders; `collections`, `heapq`, `bisect`; iterators/generators |
| **2** | Binary search — including **binary search on the answer** (the highest-yield hard pattern). Monotonic stacks. | Roofline model & arithmetic intensity. Compute AI for matmul vs. softmax vs. elementwise. Why softmax is memory-bound. | `itertools`, `functools`, decorators, closures; profiling with `cProfile`/`timeit` |
| **3** | Heaps, greedy, intervals, top-K. Linked lists (fast/slow, reversal). | **Get Colab going.** GPU execution model: grid/block/thread, warps, SMs, SIMT, divergence. First CUDA vector-add via `nvcc` in Colab. | NumPy internals: strides, views vs. copies, broadcasting, vectorization. Start `hypothesis`. |
| **4** | Trees, BST, tries, recursion + backtracking. | Triton: `vector_add`, then a **fused softmax** kernel. Understand `tl.load`/`tl.store`/masks/`BLOCK_SIZE`. Benchmark vs. PyTorch. | CPython object model, refcounting, GIL; `__slots__`, memory footprint |

**End of Phase 1 checkpoint:** solve a random medium in <25 min, cold, talking aloud. Explain to a rubber duck why a fused softmax kernel beats three separate PyTorch ops.

---

### Phase 2 — Weeks 5–8: Hard patterns + real kernels

**Goal:** graphs and DP stop being scary; you can write and *profile* a tiled matmul.

| Week | Block A: DSA focus | Block C: GPU | Block D: Python |
|---|---|---|---|
| **5** | Graphs I: BFS/DFS, grid traversal, topological sort, union-find | Memory coalescing & shared memory. Naive vs. tiled matmul — measure the gap yourself. | `asyncio` vs. threading vs. multiprocessing; when the GIL actually bites |
| **6** | Graphs II: Dijkstra, bipartite, cycle detection, multi-source BFS. Advanced backtracking. | Occupancy, bank conflicts, `__syncthreads()`. Tiled matmul in Triton with autotuning. | PyTorch internals: dispatcher, `torch.compile`, tensor memory layout, `contiguous()` |
| **7** | **DP I:** 1-D (house robber, LIS, coin change), 2-D grids, knapsack. Focus on *deriving* the recurrence, not memorizing it. | Reductions, scans, atomics. Warp-level primitives. Why reductions are a tree. | `dataclasses`, typing/generics, context managers, descriptors |
| **8** | **DP II:** strings (edit distance, LCS), intervals, tree DP, bitmask. State-machine DP. | Kernel fusion: write a fused layernorm or GELU-backward in Triton. Custom PyTorch op. | `pytest` + `hypothesis` at depth; benchmarking methodology (warmup, variance, CUDA sync) |

**DP framing to use every time** (don't memorize solutions — derive):
1. What's the decision at each step?
2. What's the minimal state that makes the future independent of the past?
3. Write the recurrence with base cases.
4. Draw the recursion tree — where's the overlap?
5. Memoize → then flip to bottom-up → then compress space.

**End of Phase 2 checkpoint:** derive a DP recurrence for an unseen problem in <10 min. Explain why your tiled matmul is faster in terms of bytes moved per FLOP.

---

### Phase 3 — Weeks 9–12: Interview conditions + a portfolio artifact

**Goal:** performance, not learning. Simulate pressure.

| Week | Block A: DSA focus | Block C: GPU | Block D |
|---|---|---|---|
| **9** | Mixed hards, random order (no topic hints — this is the real test). Design-y coding: LRU, LFU, iterators, rate limiter, min-stack. | Flash-attention style kernel in Triton: online softmax, tiling over KV. Start from the tutorial, then rewrite from memory. | ML systems design: KV cache, batching, quantization, paged attention |
| **10** | Mixed hards + **ML-flavored coding** (see below) | Profiling: Nsight Compute / `torch.profiler`. Find and fix a real bottleneck. Benchmark writeup. | ML systems design: distributed training basics, data/tensor/pipeline parallel |
| **11** | 3 full mock interviews (45 min, timed, out loud, recorded). Drill the weakest failure class from your log. | Portfolio: package a kernel + benchmarks + README into a public repo | Behavioral stories (STAR), resume/project narratives |
| **12** | 3 more mocks. Company-specific patterns. Taper — light reps, no new topics in the final 3 days. | Polish repo, write a short blog post explaining one optimization | Review the whole failure log; final weak-spot pass |

**ML-flavored coding problems** — these show up in ML/GPU loops and almost nobody practices them. Implement from scratch, pure Python/NumPy:
sliding-window attention · top-k / top-p (nucleus) sampling · BPE tokenizer · softmax with numerical stability · beam search · reservoir sampling · k-means · matrix ops without NumPy · LRU cache for a KV cache · batching/bucketing by sequence length.

---

## 4. Sundays (2h)

1. **Mock or timed set (60 min)** — from Week 5, use a live partner (Pramp / interviewing.io / a friend). Before that, self-mock: random problem, timer, camera on, talk aloud, watch it back.
2. **Failure-log retro (30 min)** — count failure classes, name the top one, pick next week's targeted problems.
3. **Plan next week (30 min)** — fill the daily log template for all 6 days. Never start a Monday deciding what to do.

---

## 5. The GPU track without a local GPU

**Weeks 1–2 need no GPU at all** — and that's not a compromise, it's the right order. Roofline and memory hierarchy are where the actual intuition lives; people who skip straight to kernels write slow ones because they never internalized bytes-per-FLOP.

**From Week 3, use free Colab (T4).** It runs `nvcc` and Triton fine, and it's enough for everything through Week 10. Constraints: sessions disconnect, so keep kernels in a git repo and `!pip install` at the top of each notebook. If you later want an A100/H100 for flash-attention work, a few hours on a rented instance (~$1–2/hr) covers Weeks 9–10.

**Core resources:**

- *Programming Massively Parallel Processors* (PMPP), Hwu/Kirk — chapters 1–6 map almost exactly onto Weeks 1–7
- Official Triton tutorials — vector add → fused softmax → matmul → flash attention (do them in order, then rewrite each from memory)
- GPU MODE lecture series (formerly CUDA MODE) — YouTube + their GitHub
- Simon Boehm's "How to Optimize a CUDA Matmul Kernel" — the single best step-by-step optimization writeup
- Horace He's "Making Deep Learning Go Brrrr From First Principles" — read this in Week 2, it's the roofline idea applied to ML

**Read-level vs. write-level:** you write Triton, you *read* CUDA C++. For these roles that's the right allocation — Triton gets you productive fast, and CUDA literacy lets you reason about what the compiler is doing.

---

## 6. Guardrails

- **Consistency beats intensity.** A 90-minute day when you're wrecked is infinitely better than a skipped day. Define a **minimum viable day**: 1 problem + B1 recall + log. ~45 min. Never break the chain.
- **One rest day every 3 weeks.** Fully off. Schedule it now: Aug 23, Sep 13, Oct 4.
- **Don't chase problem count.** A 500-problem count with 30% recall loses to 150 with 90% recall.
- **Talk out loud from Day 1.** Silent solving trains a skill you can't use in an interview.
- **Don't read solutions before the 25-minute rule fires.** The struggle *is* the training signal — bypassing it is why "I've done this problem before" doesn't translate.
- **Start mocking at Week 5, not Week 11.** Nearly everyone waits too long and discovers their communication gap with two weeks left.

---

## 7. Week-1, Day-1 concretely

Folders are already created: `solutions/`, `logs/`, `gpu/`, `patterns/`. You also have ~25 array/hashing solutions already in this repo from your last attempt — don't delete them, but **don't count them either**. Re-solve any that come up; if the old file makes it trivial, that's a signal you memorized rather than learned it.

1. `git init` if you haven't, and move the loose `.py` files into `solutions/`.
2. Copy `TEMPLATES.md` → `logs/2026-08-03.md`.
3. Block B1: skip (nothing to review yet) — instead, write down the 15 patterns you think exist and rate yourself 1–5 on each. That's your baseline.
4. Block A: 2 array/hashing problems under the full protocol. Timer on.
5. Block C: read PMPP ch. 1. In NumPy, time a 100M-element sum vs. 100M-element `a*b+c`. Ask yourself why the ratio isn't what you expected.
6. Block D: `collections` + `heapq` + `bisect` — write a 20-line cheat sheet from memory, then check it.
7. Block B2: fill the log.
