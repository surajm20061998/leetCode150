# Implement Scheduled Task Execution (Task ID + Execution Time)

**Mode:** `learn --auto` (both roles were played by AI sub-agents)
**Level:** senior | **Direction:** distributed-systems | **Date:** 2026-10-19 | **Exchange cap:** 15 (the interviewer ended at 10)
**Prep guidance:** Min-heap + condition variable locally; durable scheduling, leases, retries and idempotent effects when distributed

> The candidate got no hints from the orchestrator in any turn, and the interviewer decided on its own when to end.

---

## Exchange 1 — Scoping

**INTERVIEWER:** Let's get started. Today's problem: build a scheduled task executor. Clients call something like `schedule(taskId, executeAt)`, and the system has to run that task at the given time.

That's all the spec you get on purpose. Before you design anything, I want to hear how you'd scope it. What would you need to know about the workload, the timing guarantees, and the failure behavior before you commit to an approach? Ask me your clarifying questions. Once we agree on scope, we'll start with a single-process implementation and then grow it from there.

**CANDIDATE:** I'll group my questions. Each one comes with the assumption I'll use unless you correct me.

**Workload**
1. Scale: how many schedules are created per second, and how many tasks fire per second at peak? *Assumption: about 10k schedules/sec, and around 100M pending tasks at any time.* Firings tend to cluster. Lots of clients pick the top of the hour, so I'd plan for roughly 10x bursts at :00.
2. Horizon: are tasks scheduled seconds ahead or months ahead? *Assumption: anywhere from 1s to 1 year.* This matters because near-term and far-future tasks probably want different storage tiers.
3. What does "run the task" mean? Do we execute code ourselves, or just hand the taskId to a handler or queue? *Assumption: we dispatch to a consumer, for example a Kafka topic or an HTTP callback. Execution belongs to the client.* That keeps us a scheduler and not a compute platform.

**Timing guarantees**
4. Precision: how late can a task fire? *Assumption: p99 within about 1s of executeAt, and never early.* A 1s target allows polling; 10ms would push me to an in-memory timing wheel.
5. Ordering: if two tasks have the same executeAt, does their order matter? *Assumption: no.*

**Failure behavior**
6. Delivery semantics: *Assumption: at-least-once, with consumers deduplicating on taskId plus executeAt.* Exactly-once across a network boundary isn't realistic. I'd rather say that upfront than promise it.
7. Retries: if the handler fails, do we retry with backoff and then send to a dead-letter queue? *Assumption: yes, about 5 retries with exponential backoff, configurable per task.*
8. Missed windows: if we're down for 10 minutes, do we fire the overdue tasks late or skip them? *Assumption: fire late by default, with an optional per-task "expire after" deadline.*

**API semantics**
9. Can a task be cancelled or rescheduled? Is `schedule` idempotent on taskId? *Assumption: yes to both. Calling `schedule` again with the same taskId acts as an upsert.*
10. One-shot only, or cron-style recurring too? *Assumption: one-shot for now.* Recurring tasks can be built on top by scheduling the next run after each one fires.

If those assumptions hold, the single-process version is basically a min-heap keyed on executeAt, backed by a durable log. Does this scope match what you had in mind?

---

## Exchange 2 — Single-process implementation

**INTERVIEWER:** Your assumptions are mostly fine. Keep at-least-once, upsert on taskId, cancel, fire late after downtime, and one-shot only. I'm changing two things for now. First, set the 100M-pending and storage-tier discussion aside; we'll scale up later. Second, for this round there's no durable log. It's one process, everything lives in memory, and "execute" means handing the taskId to a fixed pool of worker threads that run a handler you don't control and that may be slow.

Write me the core of that scheduler in real code or tight pseudocode, in any language. I want to see:
- `schedule(taskId, executeAt)` with upsert semantics
- `cancel(taskId)`
- the dispatcher loop that decides when to fire, with the exact synchronization primitives and wait calls you use
- how fired tasks reach the workers

Don't describe it. Write the loop. Once it's on the page I'll walk through specific interleavings with you, so be precise about which lock is held where and what the dispatcher thread is blocked on at each point.

**CANDIDATE:** I'll write it in Java. There's one lock and one condition. The heap uses lazy deletion, and `live` is the source of truth for which entry is current.

```java
class Scheduler {
  record Entry(String id, long at, long ver) {}
  final ReentrantLock lock = new ReentrantLock();
  final Condition changed = lock.newCondition();
  final PriorityQueue<Entry> heap = new PriorityQueue<>(comparingLong(Entry::at));
  final Map<String, Entry> live = new HashMap<>();          // taskId -> current entry
  final BlockingQueue<Entry> ready = new ArrayBlockingQueue<>(1024);
  long seq = 0;

  void schedule(String id, long at) {
    lock.lock();
    try {
      Entry e = new Entry(id, at, ++seq);
      live.put(id, e);                        // any older heap entry is now stale
      heap.add(e);
      if (heap.peek() == e) changed.signal(); // new earliest: re-arm dispatcher's wait
    } finally { lock.unlock(); }
  }

  boolean cancel(String id) {
    lock.lock();
    try { return live.remove(id) != null; }   // lazy delete, no signal needed
    finally { lock.unlock(); }
  }

  void dispatchLoop() throws InterruptedException {
    while (true) {
      Entry due;
      lock.lock();
      try {
        while (true) {
          Entry h = heap.peek();
          if (h == null) { changed.await(); continue; }
          if (live.get(h.id()) != h) { heap.poll(); continue; } // cancelled/superseded
          long wait = h.at() - System.currentTimeMillis();
          if (wait <= 0) { heap.poll(); due = h; break; }
          changed.await(Math.min(wait, 1000), MILLISECONDS);   // releases lock
        }
      } finally { lock.unlock(); }
      ready.put(due);                         // may block on backpressure; lock NOT held
    }
  }

  void workerLoop() throws InterruptedException {
    while (true) {
      Entry e = ready.take();
      lock.lock();
      try {
        if (live.get(e.id()) != e) continue;  // cancelled/rescheduled while queued
        live.remove(e.id());                  // claim: point of no return for cancel
      } finally { lock.unlock(); }
      try { handler.run(e.id()); } catch (Throwable t) { log(t); }
    }
  }
}
```

Here's what the dispatcher is blocked on at each point:
- With an empty heap, it's in `changed.await()`. The lock is released, and `schedule` wakes it.
- With a future head, it's in a timed `await`, again with the lock released. `schedule` signals only when the new entry becomes the head. Spurious or early wakeups just go back through the loop and re-check.
- In `ready.put`, it holds no lock, so `schedule` and `cancel` never stall behind slow handlers.

Tradeoffs I'm choosing deliberately:
- A bounded `ready` queue means slow workers back up into the dispatcher, and tasks fire late. An unbounded queue would avoid that but risks OOM. I prefer lateness.
- A task stays in `live` until a worker claims it, so `cancel` succeeds right up to the claim. After the claim, cancel returns false. I'm not going to try to interrupt a handler that's already running.
- `executeAt` is a wall-clock time, so I cap each wait at 1s. That bounds the damage from NTP jumps. Never-early holds because I re-check against the clock before firing.
- Each reschedule leaves a stale heap entry behind. Under heavy upsert churn I'd compact the heap, or switch to an indexed heap with O(log n) remove.
- Retries are omitted. Without durability, "at-least-once" only holds while the process stays up.

---

## Exchange 3 — Interleaving: client retry during a slow run

**INTERVIEWER:** I traced cancel and reschedule against an entry that's sitting in `ready`, and also the case where an earlier insert has to wake the dispatcher. Your identity check on `live` handles both. Now walk through this one with me.

At T=1000, task X is due. The dispatcher polls it and puts it on `ready`. Worker W1 takes it, removes X from `live`, and enters `handler.run("X")`. The handler is slow and runs for 30 seconds. At T=1200, the client's original `schedule("X", 1000)` call timed out on their side, so they retry it with exactly the same arguments.

Step through your code from there. What happens in `schedule`, what does the dispatcher do next, and what is W2 doing at T≈1201? Then tell me:

1. Is that the outcome you want? In exchange 1 you described `schedule` as idempotent on taskId. Does this code keep that promise?
2. If it doesn't, what state would you need to tell "client retried the same request" apart from "client really wants X to run again," and how long would you keep that state?
3. With your current code, what should `cancel("X")` return at T=1201, and which execution would it actually cancel?

**CANDIDATE:** This is a real bug. Here's the trace.

At T=1200, `schedule("X", 1000)` runs. W1 already removed X from `live`, so to my code this looks like a brand-new task. It creates entry v2, puts it in `live`, pushes it on the heap, sees it's the head, and signals. The dispatcher wakes up, computes `wait = 1000 - 1200 < 0`, polls the entry immediately, and puts it on `ready`. At T≈1201, W2 takes it, passes the identity check, claims it, and calls `handler.run("X")`. So **two copies of X are now running at the same time**.

1. No, this isn't what I want, and the code doesn't keep the idempotency promise. Upsert only deduplicates while the task is still pending. At-least-once allows a duplicate after a failure. Here nothing failed: a client retry caused it, and the two runs overlap. That's worse than a sequential duplicate.

2. Same arguments are ambiguous on their own. I'd make the contract explicit: an execution is identified by `(taskId, executeAt)`, or by an idempotency key if the client sends one. To run X again, the client sends a new `executeAt` or a new key. That means keeping per-task state after the claim:

```java
enum St { PENDING, RUNNING, DONE }
record Rec(Entry e, St st, long finishedAt) {}
Map<String, Rec> tasks;   // replaces `live`; DONE kept until TTL

// schedule():
Rec r = tasks.get(id);
if (r != null && r.e().at() == at && r.st() != PENDING) return;  // retry: no-op
if (r != null && r.st() == RUNNING) { /* park new entry; release it when the run finishes */ }
// worker: PENDING->RUNNING on claim, RUNNING->DONE(now) after handler
// sweeper: drop DONE records older than TTL
```

The TTL has to cover the client's retry window, say 1 hour. That's a memory tradeoff: 10k/s × 1h is about 36M tombstones, which is too many for the heap. Once we add durability, this state belongs in the store with TTL expiry. I'd also never run the same taskId twice at once. A real reschedule waits for the current run to finish.

3. With the current code, `cancel` returns **false** at T=1201 because W2 has already claimed. If the call landed before W2's claim, it would return true and cancel only the duplicate. It never touches W1. A boolean can't express that, so I'd return `CANCELLED | ALREADY_RUNNING | NOT_FOUND`.

---

## Exchange 4 — Distributed: durable discovery and claim

**INTERVIEWER:** Good trace. The state model is the right direction. I'll note that "park new entry; release it when the run finishes" is still hand-waved, and we'll come back to it once there's a store underneath. Now we leave the single process.

New constraints: durability is back, with 100M pending tasks and 10k schedules/sec. At :00 you can see bursts of 100k firings/sec. There are N stateless scheduler nodes, and any one of them can be killed at any moment, including mid-dispatch. Dispatch still means handing the taskId to an execution path you don't control.

I want one thing in detail: how a due task gets discovered and claimed.
- Which durable store do you use, and what's the schema? Give me the table or key layout and the indexes.
- What does a scheduler node actually run, statement by statement, to find tasks that are due and take ownership of them? Write the queries or writes, not a description of them.
- How do you know that two nodes running that same loop at the same instant won't both dispatch the same task? Also, does this approach hold up at 100k/sec, or does it collapse onto a single hot spot?

Leave retries out for now. Discovery and claim only.

**CANDIDATE:** **Store:** I'd use sharded Postgres: 16 primaries with synchronous replicas, and 1024 logical buckets assigned by `hash(taskId) % 1024`. I'm picking it for row locks and `SKIP LOCKED`. The data is about 100M × ~200B ≈ 20GB, so size isn't the problem. Write rate is.

```sql
CREATE TABLE tasks (
  bucket      smallint, task_id text, execute_at timestamptz,
  ver         bigint,              -- bumped on every upsert
  state       text,                -- PENDING | CLAIMED | DISPATCHED
  owner       text, lease_until timestamptz,
  PRIMARY KEY (bucket, task_id));
CREATE INDEX due ON tasks (bucket, execute_at) WHERE state = 'PENDING';
CREATE INDEX stuck ON tasks (bucket, lease_until) WHERE state = 'CLAIMED';
```

**Node loop.** It runs every ~200ms, and immediately again when a batch comes back full, over the buckets the node holds:

```sql
-- 1. claim (one txn, batch of 500)
UPDATE tasks t SET state='CLAIMED', owner=$node, lease_until=now()+'30s'
FROM (SELECT bucket, task_id FROM tasks
      WHERE bucket = ANY($my_buckets) AND state='PENDING' AND execute_at <= now()
      ORDER BY execute_at LIMIT 500
      FOR UPDATE SKIP LOCKED) d
WHERE t.bucket=d.bucket AND t.task_id=d.task_id
RETURNING t.task_id, t.execute_at, t.ver;
-- 2. produce to Kafka, key=task_id, msg=(task_id, execute_at, ver); await acks=all
-- 3. fenced ack
UPDATE tasks SET state='DISPATCHED'
WHERE bucket=$b AND task_id=$id AND ver=$v AND owner=$node AND state='CLAIMED';
-- 4. reclaim tasks from dead nodes
UPDATE tasks SET state='PENDING', owner=NULL
WHERE bucket = ANY($my_buckets) AND state='CLAIMED' AND lease_until < now();
```

**Why two nodes can't both dispatch:** correctness rests on the row lock, not on bucket ownership. The first node locks the row. The second node's `SKIP LOCKED` skips it, and after the first commits, the row is no longer `PENDING`. Bucket leases (held in etcd) only spread the load. If two nodes ever overlap on a bucket, that costs efficiency, not correctness. One case remains: a node that pauses past its lease, comes back, and produces to Kafka. Step 3's fence rejects its ack, but the duplicate message is already sent. I accept that under at-least-once, and consumers dedupe on `(task_id, ver)`.

**At 100k/s:** a single table would turn the left edge of the `execute_at` index into a hotspot that every node fights over. With buckets, that's ~6k claims/sec per shard, done in about 12 batched statements per second. What worries me more is dead tuples. Every task writes 3 row versions, so autovacuum tuning and HOT updates are what I'd load-test first.

---

## Exchange 5 — The upsert that races with the claim

**INTERVIEWER:** The claim path is sound: SKIP LOCKED inside one transaction, bucketing to spread out the left edge of the index, and correctness that doesn't depend on etcd. Now I want the write path that races with it. You haven't shown `schedule()` against this table, and your fence depends on `ver`, so that write is where `ver` changes.

Write the exact upsert statement for `schedule(taskId, executeAt)`. Then trace it against three row states:

1. The row is `PENDING`. That's the easy one.
2. Node A has claimed X at ver=7 and is in step 2. The Kafka produce is in flight. The client reschedules X to one hour from now. What does your upsert set `state`, `owner`, and `ver` to? What happens to A's step 3? What does the consumer receive, and when? Does X run at the old time, the new time, or both? Does dedup on `(task_id, ver)` help here or hurt?
3. The row is `DISPATCHED`, and the client retries `schedule("X", 1000)` with the original arguments, which is the exchange-3 scenario. Does your statement fire X again?

If your answer to any of these is "it depends on a WHERE clause," write that clause.

**CANDIDATE:** One principle drives this: once a row is `CLAIMED`, a message may already be on the wire, and I can't take it back. So `schedule` must never steal a claim. It parks the new time in `next_at`, which is also how I finally pin down the "park" from exchange 3.

```sql
ALTER TABLE tasks ADD next_at timestamptz;

INSERT INTO tasks (bucket, task_id, execute_at, ver, state)
VALUES ($b, $id, $at, 1, 'PENDING')
ON CONFLICT (bucket, task_id) DO UPDATE SET
  ver        = CASE WHEN tasks.state='CLAIMED' THEN tasks.ver ELSE tasks.ver+1 END,
  execute_at = CASE WHEN tasks.state='CLAIMED' THEN tasks.execute_at ELSE $at END,
  next_at    = CASE WHEN tasks.state='CLAIMED' THEN $at END,   -- NULL otherwise
  state      = CASE WHEN tasks.state='CLAIMED' THEN 'CLAIMED' ELSE 'PENDING' END
WHERE NOT (tasks.execute_at = $at AND tasks.state IN ('CLAIMED','DISPATCHED'))
RETURNING state, ver, next_at;          -- no row returned => duplicate, no-op

-- step 3 ack, revised
UPDATE tasks SET
  state      = CASE WHEN next_at IS NULL THEN 'DISPATCHED' ELSE 'PENDING' END,
  ver        = CASE WHEN next_at IS NULL THEN ver ELSE ver+1 END,
  execute_at = COALESCE(next_at, execute_at), next_at = NULL, owner = NULL
WHERE bucket=$b AND task_id=$id AND ver=$v AND owner=$node AND state='CLAIMED';
```

1. **PENDING:** the time is replaced and `ver` goes from 7 to 8. Any old ver-7 message sitting in a retry path becomes stale.
2. **CLAIMED at ver 7:** state stays `CLAIMED`, owner stays A, ver stays 7, and `next_at` is set to +1h. A's fenced ack still matches, flips the row to `PENDING` at +1h with ver 8, and that run is dispatched an hour from now. So X runs **both** times: the old run lands now and the new one in an hour. I return `IN_FLIGHT` so the client knows the old run wasn't stopped. If I'd bumped ver instead, A's fence would fail, the row would sit `CLAIMED` until the lease expired, and the reclaim would send ver 7 a *second* time. Dedup on `(task_id, ver)` helps here, because it collapses redelivered ver-7 messages but keeps 7 and 8 distinct. Deduping on `task_id` alone would wrongly drop the real new run.
3. **DISPATCHED, same args:** the WHERE clause rejects it and nothing fires. A different `executeAt` creates a new run at ver+1.

Gaps: using `execute_at` equality as the idempotency key means "really rerun at the same time" needs a client key. `DISPATCHED` rows need a TTL sweeper. And cancel on a `CLAIMED` row can only clear `next_at`.

---

## Exchange 6 — Retries and DLQ

**INTERVIEWER:** Parking in `next_at` without bumping `ver` is the right call. Your reasoning about why bumping would trigger a second ver-7 send through reclaim is correct. Still, you have a hole. While X is CLAIMED for 1000, a client moves it to +1h and then changes its mind and moves it back to 1000. Your WHERE clause rejects that second call as a duplicate, so `next_at` stays at +1h and X runs an extra time that nobody wants. Keep that in mind; I'm not going to chase it now.

Here's the bigger gap. Your row reaches `DISPATCHED` as soon as Kafka acks. All that ack tells you is that the message landed in a topic. It doesn't tell you X succeeded. Suppose the consumer pulls X at ver 8 and the handler throws, or the consumer crashes halfway through.

- Who owns the retry: the consumer, the scheduler, or Kafka redelivery? Write the state transitions and the statement that re-arms X for its next attempt.
- Where are the attempt count and backoff stored, and what happens after the last attempt fails?
- A retry has the same `(task_id, ver)` as the attempt that failed. How does the consumer's dedup tell "retry after a failure" apart from "redelivery of a message that already succeeded"?

**CANDIDATE:** Noted on the move-back hole. Comparing against `next_at` as well as `execute_at` would fix it, and I'll leave it there.

**The scheduler owns retries.** I don't want Kafka redelivery doing it. Redelivery blocks the partition behind the failing message and has no backoff. The consumer commits its offset once it has the message, and then reports the outcome on a results topic. A Kafka ack only moves the row to `DISPATCHED` with a deadline. Getting to `DONE` takes a reported success. If the consumer crashes, no report arrives and the deadline expires, so the sweeper treats a crash the same as a failure.

```sql
ALTER TABLE tasks ADD attempt int DEFAULT 0, ADD max_attempts int DEFAULT 5;
-- step-3 ack also sets lease_until = now() + handler_timeout; msg = (id, ver, attempt)

-- success report
UPDATE tasks SET state='DONE' WHERE bucket=$b AND task_id=$id
  AND ver=$v AND attempt=$a AND state='DISPATCHED';

-- failure report, or sweeper on DISPATCHED with lease_until < now()
UPDATE tasks SET
  attempt    = attempt + 1,
  state      = CASE WHEN attempt+1 >= max_attempts THEN 'DEAD' ELSE 'PENDING' END,
  execute_at = now() + least(interval '1s' * 2^attempt, interval '1h')
                       * (0.5 + random()/2)            -- capped expo + jitter
WHERE bucket=$b AND task_id=$id AND ver=$v AND attempt=$a AND state='DISPATCHED';
```

PENDING --> CLAIMED --> DISPATCHED --> DONE. From DISPATCHED, a failure or timeout goes to PENDING with attempt+1, or to DEAD once attempts run out.

Attempt count and backoff live on the row, so a retry goes back through the same claim path with no extra machinery. A `DEAD` row stays put for inspection. I also emit it to a DLQ topic and alert. Fencing on `attempt` means a late report from an attempt that already timed out is ignored.

**Dedup:** the consumer dedups on *success*, not on receipt. It keeps a completion record keyed on `(task_id, ver)`. A failed attempt never writes one, so attempt 2 runs. A redelivery after a success finds the record and just re-reports success. Ideally the handler writes that record in the same transaction as its side effects. If it can't, the gap between "side effects done" and "record written" is a real hole, and the handler has to be idempotent.

One choice I'm making: once a reschedule bumps `ver`, the old run's retries get fenced out and are dropped.

---

## Exchange 7 — Slow-but-alive handler vs lease expiry

**INTERVIEWER:** Retry state on the row, fencing on `attempt`, and dedup on success instead of receipt are all solid. Now trace a handler that is slow but still alive.

handler_timeout is 60s. Consumer C1 picks up X at ver 8, attempt 0, and starts the handler. The handler is healthy, just slow because a downstream dependency is degraded, and it takes 90s. At t=60 the sweeper sees the DISPATCHED lease has expired. Step through it from there:

1. What does the sweeper write? When does X get claimed and dispatched again, and what does consumer C2 do when it checks your completion record at that moment?
2. At t=90, C1 finishes and the side effect has happened. What happens to C1's success report? What happens to C1's completion-record write? Then what does C2 do?
3. Your fence on `attempt` protects the tasks row. Does anything stop C1 from applying its side effect after attempt 0 has been fenced out? If you think something should, tell me where the fence is checked and who checks it. Keep in mind that you don't control the handler or its downstream.

I'm not asking for a bigger timeout. Explain what the guarantee is when a timeout is wrong.

**CANDIDATE:** Short answer: the timeout is a failure detector. It doesn't kill anything. When it's wrong, X runs twice and the two runs overlap.

```
t=0   C1 --> handler(X, v8, a0) .......................... side effect, t=90
t=60  sweeper: a0 --> a1, PENDING, execute_at = now + ~1s
t=61  claim --> Kafka --> C2: no record for (X,8) --> handler(X, v8, a1) ...
t=90  C1: report(a0) --> fenced, 0 rows | record (X,8) INSERT ok
t=9x  C2: record INSERT conflicts | report(a1) --> DONE
```

1. The sweeper runs my failure statement. Attempt goes to 1, the row goes back to PENDING, and backoff is about 1s. Around t=61 it gets reclaimed and dispatched. C2 checks the completion record for (X,8) and finds nothing, because C1 hasn't finished yet, so C2 starts the handler. This is the exchange-3 overlap again, now across machines.
2. C1's success report matches 0 rows because the row is at attempt 1, so it's dropped. C1's completion-record write succeeds, since the record is keyed on (task_id, ver) and not on attempt. C2 already passed its check at t=61. If the handler writes the record and the side effect in one transaction with insert-if-absent, C2's transaction aborts, its side effect rolls back, and it reports success. If the side effect goes to an external system, it happens twice.
3. Nothing in my design stops C1. The `attempt` fence only protects my row. A fence only works where the write lands. The downstream would have to reject stale tokens (Kleppmann-style fencing), or dedupe on a key. I don't control it, so I can't enforce that.

What I can do:
- **Heartbeat lease renewal.** C1 keeps extending `lease_until` while the handler is alive. Then slow-but-alive never trips the sweeper, and only real partitions or long GC pauses still cause overlap. That makes overlap less likely, but it can still happen.
- **A stable idempotency key.** Pass `(task_id, ver)` to the handler, not `attempt`, so overlapping attempts collide at the downstream.

The honest guarantee: at-least-once, possibly concurrent, with a stable key per logical run. Exactly-once effect only holds where the downstream honors that key.

---

## Exchange 8 — The 12:00 burst

**INTERVIEWER:** That's an honest statement of the guarantee. Now let's put load on the whole pipeline.

It's 11:59:59. 6M tasks have execute_at = 12:00:00 exactly, and they're spread evenly across your 1024 buckets. Your SLO is p99 lateness ≤ 1s. Most of these tasks call the same downstream service, and that service starts timing out above about 20k req/s.

Walk me through the first 60 seconds with numbers, stage by stage: claim, ack, Kafka, consumers, results topic, and the success/failure updates.
- How many Postgres row writes per second does each shard take at the peak, including the retry path? Where does lateness pile up first?
- The downstream starts timing out. Trace what your retry and lease-expiry machinery does to the load on it from t=60s on. Does the system recover on its own, or does it amplify?
- What is the actual lateness distribution you'd deliver, and what would you change to protect the downstream? Who decides that, you or the client?
- How would you know any of this is happening? Name the specific metric, measured from which timestamp to which, and say where it's emitted.

Numbers, not adjectives.

**CANDIDATE:** First, a 1s p99 is impossible for this burst. The downstream tops out at 20k/s, so the last of the 6M tasks can't start before 6M/20k = 300s. What I can choose is whether we degrade to about 300s or to something much worse.

Assumptions: there are 16 shards, so 375k due rows per shard. One shard sustains about 15k row writes/s with batched statements and a sync replica. That's a guess I'd load-test. Every attempt costs 3 writes: claim, ack, and the DONE or failure update. The ack and result updates I wrote are per-row, so they have to be batched with `unnest`, or the shard caps far lower.

```
stage           | no limiter                 | with limiter
----------------+----------------------------+---------------------
PG writes/shard | 15k/s (saturated)          | 1,125 tasks/s = 3.4k/s
claim->Kafka    | 5k/s/shard = 80k/s, 16MB/s | 18k/s
consumers->down | 80k/s offered, 4x the knee | 18k/s
first-try drain | 375k/5k = 75s per shard    | 6M/18k = 333s
```

**Where lateness piles up:** In Postgres claim, a shard needs 75s to drain even when the downstream is healthy. Then the downstream collapses, and goodput probably falls below 20k/s.

**Retry trace:** Timeouts produce failure reports, and backoff re-arms them after 0.5-1s, then 1-2s, 2-4s, 4-8s. Heartbeats keep the sweeper away, but the handler's own client timeouts still fail. Retries compete with first attempts for the same 15k writes/s. Worst case is 15 writes per task, so 5.6M per shard, which is 375s of saturation. max_attempts limits amplification to 5x, so it doesn't spiral forever. But it's metastable: it only recovers when millions of tasks reach DEAD. That's the worst outcome.

**Fixes:**
1. A per-destination token bucket at the claim, set to 18k/s (90% of the knee). Because buckets are even, I'd split it statically at 1,125/s per shard. Waiting as PENDING costs nothing, but claimed rows use up leases.
2. A retry budget: retries get at most 10% of the destination's tokens. A circuit breaker re-arms tasks without `attempt++`.
3. Result: lateness is roughly uniform from 0 to 333s, with p50 ≈ 167s, p99 ≈ 330s, and no DEADs caused by overload.

**Who decides:** The downstream owner sets the rate. The client sets its tolerance (`max_lateness`) or a schedule-time `jitter_window`. I enforce both, and the SLO I'd commit to is min(1s, backlog/dest_rate).

**Metrics:**
- `start_lateness` = handler start minus execute_at. The consumer emits it per destination, and it's the SLO metric.
- `dispatch_lateness` = claim commit minus execute_at, emitted by the scheduler. Comparing it with `start_lateness` separates Kafka/consumer queueing from claim delay.
- `oldest_due_age` per bucket, taken from the claim query's first row. Alert if it's above 1s for 30s.
- `retry_ratio` (claims with attempt>0 divided by all claims) and DEAD/s, per destination.

---

## Exchange 9 — Multi-tenant head-of-line blocking

**INTERVIEWER:** The 300s floor is the right place to start, and your arithmetic holds together. But your limiter doesn't fit your own claim query.

Your claim query is `WHERE bucket = ANY(...) AND state='PENDING' AND execute_at <= now() ORDER BY execute_at LIMIT 500`. Nothing in it knows about destinations. Now add a second tenant: 50k tasks, due at 12:00:30, that call a completely healthy service. The rate limiter says "1,125/s per shard for destination D."

1. Where in the loop is that limit enforced? Do you claim 500 rows and then hold back the D rows? Skip them? Release them? What happens to the healthy tenant's 12:00:30 tasks, which sit behind roughly 375k earlier D rows in every bucket's `due` index? Give me their lateness.
2. If you fix it, show the schema or index change and the new claim statement. Then tell me what that change costs you. Think about how many destinations you can support, the per-destination scans per poll, and what happens to the "spread evenly across buckets" assumption your static 1,125/s split depended on.

**CANDIDATE:** You're right. The limiter was written on top of a claim query that has no way to apply it.

**1. As written:** the `LIMIT 500` returns the 500 oldest due rows, and every one of them is D. None of my three options works.
- **Hold:** the claimed rows burn their 30s leases while they wait. At 1,125/s, a 500-row batch takes about 0.45s to drain per shard, so the next poll grabs another 500 D rows. The node ends up with a growing pile of claimed D rows, and leases start expiring into reclaim churn.
- **Release:** that costs 2 writes per row per poll and re-selects the same 500 rows forever. It's a livelock.
- **Skip in SQL:** I can't, because there's no `dest` column to filter on.

In every case the healthy tenant waits until D drains below 12:00:30. That's about 375k rows / 1,125/s ≈ 333s, so its **lateness is about 303s** even though its service is healthy. That's head-of-line blocking across tenants.

**2. Fix: one claim lane per rate-limited destination.**

```sql
ALTER TABLE tasks ADD lane text NOT NULL DEFAULT 'default'; -- = dest if limited
DROP INDEX due;
CREATE INDEX due ON tasks (bucket, lane, execute_at) WHERE state='PENDING';

-- per (bucket, lane) with tokens k > 0, oldest-due lane first
UPDATE tasks t SET state='CLAIMED', owner=$node, lease_until=now()+'30s'
FROM (SELECT bucket, task_id FROM tasks
      WHERE bucket=$b AND lane=$lane AND state='PENDING' AND execute_at<=now()
      ORDER BY execute_at LIMIT least($k,500) FOR UPDATE SKIP LOCKED) d
WHERE t.bucket=d.bucket AND t.task_id=d.task_id RETURNING ...;
```

To find the active lanes in a bucket, I'd use a recursive-CTE skip scan on `due` and cache the result for about 1s.

With this change, the healthy tenant goes through `default`. Its 50k tasks come to about 3.1k per shard. That's roughly 9.4k writes/s on top of D's 3.4k, which is under my 15k guess, so I'd expect lateness of about 1–2s. That number is tight, and I'd load-test it.

**Costs:**
- **Scan fan-out.** A node does buckets × lanes probes per poll. With 64 buckets × 1,000 lanes at 5 polls/s, that's 320k probes/s, which won't work. So only destinations that have a limit get their own lane, capped at about 50. The long tail shares `default`. Moving a destination into its own lane means rewriting `lane` on its pending rows.
- **The even-spread assumption breaks.** A small tenant hits only a few buckets, so a static 1,125/shard split wastes tokens on empty shards. I'd replace the static split with a central per-destination token service. Nodes lease tokens in chunks of about 100, weighted by their backlog for that lane. That puts a token service in the hot path, and if it's unreachable, nodes fall back to the static split.
- **Ordering.** There's no longer any ordering across lanes. I never promised any, but `oldest_due_age` now has to be tracked per lane.

---

## Exchange 10 — Close

**INTERVIEWER:** ENDING: Okay, we're at time, so I'll stop there. We went from the in-memory dispatcher to durable claiming, fencing, retries, the guarantees on side effects, and then the burst and multi-tenant cases. Thanks for working through the traces in detail. The recruiter will be in touch about next steps. Do you have anything quick you'd like to ask me before we wrap up?

---

# Retrospective (critical staff-level observer)

**1. What the candidate did well**
- **The in-memory core is correct.** One lock and one condition, lazy deletion with a reference-identity check against `live`, and a re-check of the clock before firing so tasks never fire early. `ready.put` runs outside the lock, so backpressure never stalls `schedule` or `cancel`. With a single dispatcher, `signal` (not `signalAll`) only when the new entry becomes the head is correct. The 1s cap on the timed wait limits damage from wall-clock jumps.
- **Fencing is reasoned from first principles.** Parking the new time in `next_at` instead of bumping `ver` on a CLAIMED row is backed by a concrete failure: bumping would make reclaim send ver 7 a second time. The `attempt` fence and "dedup on success, not on receipt" are both sound. The admission that "a fence only works where the write lands" is the senior-level insight.
- **The burst analysis starts from the real limit.** 6M / 20k/s = a 300s floor. The arithmetic per shard holds, the candidate named retry metastability, and they correctly separated `dispatch_lateness` from `start_lateness`.

**2. What a critical reviewer would flag**
- **The exchange-3 bug comes back.** Exchange 6 added DONE and DEAD states, but the upsert's guard is still `NOT (execute_at=$at AND state IN ('CLAIMED','DISPATCHED'))`. A client retrying `schedule("X",1000)` after X reaches DONE matches no guard. The row flips to PENDING with ver+1 and X fires again. The upsert also never resets `attempt`, so a DEAD task that gets rescheduled starts at attempt 5 and goes straight back to DEAD on its first failure. An upsert on a DISPATCHED row with a near-term time also lets two runs overlap, which contradicts "never run the same taskId twice at once."
- **The 30s CLAIMED lease is shorter than Kafka's default produce timeout** (`delivery.timeout.ms` = 120s). Reclaim can reset a row while its produce is still retrying, and another node then sends the same ver again. Dedup absorbs the duplicate, but the lease should be longer than the produce timeout, or the node should abort the produce when its lease runs out.
- **The claim query and indexes fail during the burst.** `bucket = ANY($my_buckets) … ORDER BY execute_at LIMIT 500` cannot read the `(bucket, execute_at)` index in order across many buckets. With roughly 375k due rows per shard, every poll becomes a top-N sort over all of them, so the loop should claim per bucket. The sweeper for timed-out DISPATCHED rows has no index (`stuck` covers only CLAIMED). Heartbeat writes are left out of the 15k writes/s budget.
- **Pacing.** Ten exchanges of finished SQL, Java, and tables is not what a senior candidate produces live in 45 minutes. The etcd bucket leases, the lane skip-scan, and the token service lean toward over-engineering.

**3. Where the interviewer could have pushed harder**
- They should have re-checked the exchange-5 upsert against the DONE/DEAD states added in exchange 6, and required a fix for the move-back hole instead of letting it go.
- They could have asked what clock decides "never early." The answer is each shard primary's `now()`, which shifts on failover and with skew between shards. They also never asked how 100M far-future rows stay out of the hot `due` index.

**4. Takeaways for senior-level practice**
- **Heap + condvar:** write about 25 lines covering a timed await on the head, a signal only when the head changes, re-checks against the clock, lazy delete with a version, and dispatch outside the lock. Say "wall-clock target, monotonic wait" once.
- **Durable scheduling:** a table indexed on `(bucket, execute_at)` for PENDING rows, a per-bucket `FOR UPDATE SKIP LOCKED` claim, and a far-future tier kept out of the hot index.
- **Leases:** the lease must be longer than the worst-case dispatch time. Reclaim on expiry, fence with `(ver, owner)`, and admit that a node that pauses past its lease can still send a duplicate.
- **Retries:** the scheduler owns them. Keep attempt and backoff with jitter on the row, fence on attempt, send exhausted tasks to DEAD/DLQ, and add a retry budget so overload doesn't amplify.
- **Idempotent effects:** use one key per logical run, `(task_id, ver)`. Re-check every terminal state in the upsert guard. Exactly-once effects exist only where the downstream honors that key, so say this plainly.

---

**Next step:** `/system-design mock --level=senior Implement scheduled task execution from task ID and execution time`. Answer the question yourself under scoring. Aim to write the heap and condition-variable loop in under 8 minutes, and to state the upsert guard for every terminal state.
