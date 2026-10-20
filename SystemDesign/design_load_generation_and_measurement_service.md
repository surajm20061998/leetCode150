# Design a Distributed Load-Generation and Measurement Service

**Mode:** `learn --auto` (both roles were played by AI sub-agents)
**Level:** senior | **Direction:** distributed-systems | **Date:** 2026-10-19
**Prep guidance:** control plane, paced agents, result ingestion, safe limits, bottleneck isolation, latency histograms

> **How this run differed from a normal one:**
> - It ended after 9 exchanges. Once every guidance area was covered, the orchestrator told the interviewer to close.
> - In exchanges 4 and 5, the orchestrator's prompts listed the points the candidate should cover, so those two answers are more polished than a live candidate would produce unprompted. From exchange 6 on, the candidate answered without hints.

---

## Exchange 1

**INTERVIEWER:** Thanks for coming in. Today's question: design a distributed load-generation and measurement service. Engineers inside the company use it to drive traffic at their own services and measure how those services behave under load.

We have about 45 minutes. Take a couple of minutes first to work out scope. Ask me whatever you need, then tell me what you think the requirements are before you start drawing anything. Go ahead.

**CANDIDATE:** Thanks. Before I draw anything I'd like to pin down scope. I'll give an assumption with each question so you can just confirm it or correct it.

**Scale**
1. Peak load from one test? I'm assuming up to about 1M RPS, which is roughly 200–500 generator workers. Typical tests are much smaller, around 1–50k RPS.
2. How many tests run at once across the fleet? I'm assuming about 100 concurrent tests and around 10M RPS in aggregate.
3. How long do tests run? Usually 5–60 minutes, with soak tests running up to 24 hours.

**Workload**
4. Which protocols? HTTP/1.1, HTTP/2 and gRPC to start, with a plugin interface for others like Thrift or raw TCP.
5. Open-loop or closed-loop load? I'll treat open-loop (a fixed arrival rate) as the main mode so we don't get coordinated omission. Closed-loop (N virtual users) would be an option. Tests also need load profiles: ramp, step and spike.
6. Are tests simple single requests or scripted? I'm assuming mostly single-request templates with parameterized payloads, plus light multi-step scenarios.

**Measurement**
7. Which metrics? Throughput, error rate by status code, and latency at p50, p90, p99 and p99.9. Percentiles have to be correct when merged across workers, so I'd use mergeable histograms like HDR or DDSketch, not averages of percentiles.
8. How fresh do results need to be? Live dashboards about 5 seconds behind, and a final report available within about a minute of the test ending.
9. How long do we keep results? Aggregated results for about a year so runs can be compared over time. I'd skip per-request raw logs, or keep only a sample of them.

**Safety and control**
10. Target safety: I'm assuming only the owning team can test a target, there are per-target RPS caps, and production targets need explicit approval. Tests should auto-abort when error rate or latency SLO thresholds are breached, and there should be a global kill switch that stops traffic within about 5 seconds.
11. How accurate does the rate need to be? Within about ±5% of the requested RPS. Generators also need to report their own saturation so we don't blame the target for slowness that's really ours.

**Out of scope unless you want them:** browser/UI load testing and CI gating.

Do these numbers look right, especially the 1M RPS per test and 100 concurrent tests?

---

## Exchange 2

**INTERVIEWER:** Good scoping. Most of this holds. A few corrections:

- **Scale:** Keep 1M RPS as the ceiling for a single test. Plan for about 30 tests running at once, not 100, but expect a couple of the big tests to overlap. Aggregate peak is around 3M RPS.
- **Fleet:** Generators don't get dedicated hosts. They run on a shared Kubernetes pool that other batch workloads also use, so expect noisy neighbors and pods getting preempted in the middle of a test. Targets are spread across three regions.
- **Duration, protocols, load profiles:** Your assumptions are fine. Scripting is single-request templates only. Multi-step scenarios are out of scope.
- **Freshness and retention:** Agreed, 5s live and about 1 minute for the final report. Aggregates are kept for a year. Assume no raw per-request logs.
- **Safety:** Owner-only access and per-target caps, yes. Production tests do happen, so treat them as a first-class case, not an edge case. The kill switch has to work even if the control plane itself is degraded.
- **Out of scope:** Browser testing and CI gating are both out.

Now give me the high-level design. Walk me through the main components and what happens to a test from submission to final report. Stay at the box-and-arrow level for now. We'll go deep later.

**CANDIDATE:** Here's the end-to-end flow. Load and metrics traffic run on separate paths from the control plane.

```
 Engineer --(spec)--> +-------------------+ --> +-------------------------+
                      | Test API          |     | Control DB (Postgres)   |
                      | authz, owner,     |     | specs, runs, approvals, |
                      | caps, prod appr.  |     | target caps             |
                      +-------------------+     +-------------------------+
                                |                          ^
                                v                          |
                      +-------------------+                |
                      | Scheduler         |----------------+
                      | admit vs quota,   |
                      | split RPS/region  |
                      +-------------------+
                                | run plan (x3 regions)
                                v
 +----------------------------- REGION (x3) ------------------------------+
 |  +---------------------+  rate shares   +-----------------------+      |
 |  | Region Controller   |--------------->| Agent Pods (k8s,      |=========> Target
 |  | (k8s operator,      |<- - heartbeat -| preemptible; Go,      |      |    Service
 |  |  lease, rebalance)  |    5s lease    | open-loop, HDR)       |      |
 |  +---------------------+                +-----------------------+      |
 |                                            |               ||          |
 |  +---------------------+     poll 1s       |               ||          |
 |  | Kill Store (etcd)   |<- - - - - - - - - +               ||          |
 |  +---------------------+                                   ||          |
 +-----------^-----------------------------------------------||----------+
             |  kill (also: on-call CLI, direct)               ||  1s HDR
             |                                                 vv  histograms
 +---------------------+   +----------------------+   +-------------------+
 | Guardrail Evaluator |<--| Stream Aggregator    |<==| Metrics Bus       |
 | (err/SLO -> abort)  |   | (Flink, merge 1s HDR)|   | (Kafka)           |
 +---------------------+   +----------------------+   +-------------------+
                               ||              |
                               vv              v on run end
                      +----------------+  +---------------------------+
                      | Live TSDB      |  | Report Builder -->        |
                      | (dashboards)   |  | Results Store (PG + S3)   |
                      +----------------+  +---------------------------+
```

**Flow.** The Test API checks ownership, the per-target cap and prod approval, then writes the run to Postgres. The Scheduler admits the run against fleet quota and splits its RPS across regions. Each Region Controller is a k8s operator. It launches agent pods, gives each one a rate share, and sets a synchronized start time. Agents fire open-loop and ship one HDR histogram per second, keyed by run_id, to Kafka. Flink merges these into 1s windows. The merged windows feed live dashboards and a guardrail evaluator that can abort the run. When the run ends, the Report Builder waits for each agent's final flush (30s timeout), then writes the report.

**Sizing.** I'm budgeting about 5k RPS per 2-vCPU agent, run at ≤60% CPU because of noisy neighbors. That's about 200 pods for a 1M test and about 600 for the 3M aggregate. Add roughly 25% spare pods to cover preemption, so around 750. Metrics volume is about 750 msgs/s at roughly 3KB each, so ~2MB/s, which Kafka handles easily. Raw per-request events would be 3M/s at 100B each, so 300MB/s. That gap is why the agents pre-aggregate.

**Preemption.** If a heartbeat stops, the controller moves that agent's rate share to a spare within about 3s. The report marks that gap so we don't blame the target for it.

**Kill switch.** It has three independent layers:
1. **Kill flag.** It lives in a regional etcd that agents poll every second. On-call can write to it directly.
2. **Dead-man lease.** If an agent can't renew its 5s lease, it stops. A degraded control plane therefore stops load instead of leaving it running.
3. **Signed cap.** The plan carries a signed hard RPS cap that each agent enforces locally.

For prod runs, guardrails are tighter and ramps are mandatory.

**Tradeoff.** Pushing rate shares from the controller is simpler than agents coordinating among themselves. The cost is a ~3s rebalance gap, which fits within the ±5% accuracy target.

Where would you like to go deep? The options I see are rate accuracy under preemption, the metrics path and correct percentiles, or kill-switch and prod safety.

---

## Exchange 3 — Paced agents & bottleneck isolation

**INTERVIEWER:** Let's start inside one agent. You said "open-loop, so no coordinated omission," but you haven't told me how that's actually achieved, so I'm going to push on it.

Take a single agent pod. It owns 5,000 RPS of a run. It's on the shared pool, and a noisy neighbor causes CFS throttling for about 80ms. During that window the target is healthy. A few seconds later the target itself slows down, and p99 goes from 20ms to 2s.

Walk me through the agent's send path concretely:

1. How does it decide when each request is sent? What does it do with requests whose scheduled time has already passed?
2. Where does the latency clock start for each request? Is it the moment the request is actually written to the socket, or something else? What does that choice do to the p99.9 in your HDR histogram in each of the two scenarios?
3. When the target slows to 2s, how many requests are in flight on that pod, and what limits that number? Connections, goroutines, file descriptors? What happens when you hit that limit?

Then tell me how a reader of the final report could tell the first scenario (our generator stalled) from the second (the target really degraded). Which signal makes the difference, and where does it show up in the report?

**CANDIDATE:** **1. Scheduling.** Each request gets an intended start time in advance: t_i = t0 + i/rate, or with Poisson jitter if the test asks for it. One pacer goroutine per pod walks that schedule with a monotonic clock and hands each slot to a worker pool. The pacer never waits for responses. When a slot's time has already passed, as it will after an 80ms throttle, the pacer still sends it, but catch-up is capped at 2x the nominal rate so the backlog doesn't hit the target as one spike. If lag goes past 1s, we stop sending those slots and count them as `missed_generator`.

**2. Clock start.** Every response produces three numbers:
- `response_latency` = done − intended. This is the headline number, corrected for coordinated omission.
- `service_latency` = done − socket write.
- `send_lag` = socket write − intended.

Scenario 1 (our stall): roughly 400 requests are delayed by 0–80ms. That's about 0.1% of a minute's traffic, so corrected p99.9 rises to around 60ms while service p99.9 stays at about 20ms. Scenario 2 (target slows): both histograms go to about 2s, and send_lag stays near zero.

**3. In-flight.** By Little's law, 5,000 RPS × 20ms is about 100 requests in flight. At 2s it's 5,000 × 2 = 10k. Per pod we enforce:
- a hard cap of 10k in flight
- a 5s request timeout
- HTTP/2 at 100 streams per connection (about 100 connections), or an HTTP/1.1 pool of up to 10k sockets
- a file-descriptor ulimit of 64k

Goroutines are not the constraint, since 10k × 8KB is about 80MB. When we reach the cap, the pacer does not block, because blocking would bring coordinated omission back. Instead the slot is recorded as `dropped_inflight_cap`, a distinct outcome with its own count in the report, so the attempted rate stays honest.

**Telling them apart.** Agents also export cgroup `cpu.stat` throttling and pacer lag. The report has a "Generator health" lane on the same timeline as latency:
- Scenario 1: one pod's send_lag p99 jumps to 80ms and its throttle counter rises, while service latency stays flat on every agent. That window is shaded "generator-suspect".
- Scenario 2: send_lag stays flat, and service latency rises on every agent in every region at the same moment. That pattern means the target degraded.

If generator-suspect windows add up to more than 1% of the run, the whole report is marked "low confidence".

One part I'm unsure about is the 2x catch-up cap. It's a judgment call between staying faithful to the requested rate and avoiding a burst we created ourselves.

---

## Exchange 4 — Latency histograms

**INTERVIEWER:** Good on the three timings, but note that whenever `missed_generator` or `dropped_inflight_cap` slots never reach a histogram, your corrected tail looks better than what really happened. Keep that in mind for what follows.

Now the numbers themselves. Picture a 30-minute run: 200 agents, each emitting a latency histogram every 1 second. Latencies range from 300µs (cache hits) to a 5s timeout. Product wants three things: (a) p99.9 for the whole run, (b) p99 per region per 10-second window on a live dashboard, and (c) a guarantee that the reported p99.9 is within 1% of the true value.

Be concrete:
1. What histogram do the agents emit? Give the exact configuration: lowest and highest trackable value, precision, and the approximate serialized size per agent per second. What does that cost across the fleet?
2. Show how you get (a) and (b) from the 1s per-agent pieces. Which operations are mathematically valid here, and which common shortcut gives you a wrong answer?
3. Does your configuration actually meet the 1% guarantee at both 300µs and 4.8s? If someone suggested DDSketch instead, what would change?

**CANDIDATE:** **Censored slots first.** You're right. Slots marked `missed_generator`, `dropped_inflight_cap` or timed out get recorded in the corrected histogram at 5s, the worst case, and also keep their own counters. If those slots add up to more than 0.1% of attempts, p99.9 is reported as "≥5s (censored)" and not as a number.

**1. Config.** HdrHistogram in µs units: lowest 1µs, highest 10s (above the timeout, so nothing gets clamped), 3 significant digits. That gives 2,048 sub-buckets, or 1,024 per octave, which is about 0.1% resolution. The dense array is about 25k counters (~200KB in memory), but a 300µs–5s distribution at ~5k RPS fills maybe 1–2k buckets. The V2 encoding (zigzag varint, zero runs) plus deflate comes to about 2–3KB per agent per second. Fleet: 200 × 3KB ≈ 600KB/s (~5Mbps). Over 30 min that's about 1.1GB, which is trivial, so we keep the raw 1s pieces for drill-down.

**2. Merge.** Merging means adding counts bucket by bucket. It's exact and associative, and the header carries a config hash so mismatched configs are rejected.
- (a) Sum all 360k pieces, keeping a running total, then read p99.9 once.
- (b) Per region, sum the agents' histograms over ten 1s pieces, bucketed by intended-send time, with a ~3s watermark. Late data revises the panel.

Subtraction is also valid, which gives cheap sliding windows. The wrong shortcut is averaging percentiles: mean of per-agent p99s, p99 of window p99s, or traffic-weighted means. None of these is a quantile of the merged population.

**3. Accuracy.** Values under 2,048µs are exact to 1µs, so 300µs is within ~0.3%. At 4.8s the bucket width is about 4ms, or ~0.09%. That meets the guarantee with margin. Two significant digits would come in at ~0.7%, which is too tight. Note that "within 1%" here means *value*-relative error. Rank is exact because we keep full counts. That's unlike t-digest or KLL, which have rank error. With 1.8B samples, sampling noise is negligible, so the real risk is censoring, not the sketch.

**DDSketch** at α=0.5%: γ≈1.01, so ln(16,667)/0.01 ≈ 970 log buckets. It's mergeable with the same α, has no fixed highest value, and comes out at about 1–2KB, which is smaller. Its bucket count stays bounded by collapsing the lowest buckets, which only hurts low quantiles. The tradeoff is a log() on every record instead of index arithmetic. Either works. I'd keep HDR for compatibility with existing tooling.

---

## Exchange 5 — Result ingestion

**INTERVIEWER:** Solid. Recording censored slots at 5s closes the gap I flagged, and exact bucket-wise merging is the right answer.

Now the path those pieces take. It's minute 22 of a 30-minute production run. GKE preempts 15 agent pods in us-east. Each one gets SIGTERM with a 30s grace period, but each is holding about 2s of unflushed histograms. On top of that, its Kafka producer is in the middle of retrying after a broker leader election, so some 1s pieces land twice and some never land at all. The controller reschedules replacement pods with new pod IDs, and they pick up the same rate shares. Meanwhile Flink fails over and restores from a checkpoint that is 40s old. When the run ends, three agents never send a final flush, and the Report Builder's 30s wait times out.

1. What makes a 1s piece idempotent end to end? Give the exact dedup key and say where it's enforced. Is Flink's exactly-once enough on its own?
2. How does the Report Builder know the report is complete, as opposed to missing pieces? What does the report show for the gaps?
3. For the preemption seconds, do the replacement pods double-count or leave holes?

**CANDIDATE:** **1. Dedup key.** `(run_id, shard_id, epoch, sec)`. `shard_id` is the logical rate share, not the pod. `epoch` is the shard's lease generation from etcd. `sec` is the intended-send second since t0. Pod IDs never appear in it. Enforcement is layered:
- Kafka idempotent producer (`acks=all`, idempotence on). This removes retry duplicates, but only within one producer session. A restarted pod gets a new producer ID, so it isn't enough.
- Flink keeps keyed state of seen `(shard_id, sec)` with a TTL of run length. It drops duplicates and stale epochs.
- The sink upserts on a primary key `(run_id, shard_id, sec)`, and S3 objects use that key as their path. Rewrites are no-ops.

Flink exactly-once covers only Flink's own state and its transactional sinks. Two copies the producer already wrote are two distinct offsets, so Flink counts both correctly, twice. On the 40s restore, Flink rewinds offsets and replays. The upsert sink absorbs that, and live panels revise for about 40s. Agents' local hard caps still protect the target while guardrails are blind.

**3. Preemption (before 2).** The controller hands shard S over at a fence second F: the old owner keeps `sec < F` at epoch E, and the new owner gets `sec ≥ F` at E+1. Pieces that carry E for `sec ≥ F` are rejected as zombie writes, so seconds can't be double-counted. On SIGTERM the agent stops its pacer first, then flushes its 2s buffer with a final piece carrying `last_sec`, all well inside the 30s grace period. The seconds between `last_sec` and F are holes: about 3s × 15 shards × 5k RPS ≈ 225k requests. We report them and never interpolate. Each piece also carries a cumulative sent counter, so a lost piece still tells us how many requests went unmeasured.

**2. Completeness.** The ownership ledger in Postgres records `(shard, epoch, start_sec, end_sec)`, so expected = 200 × 1,800 = 360k pieces, and received = distinct keys in the store. In this scenario about 45 + 15 pieces are missing, so coverage is about 99.98%. The report publishes as *provisional* at end+60s. It shows coverage %, gaps shaded per region, unmeasured-but-sent counts, and p99.9 as received plus censored. It's re-finalized if late pieces land, since Kafka retains them for 7 days. Below 99.5% coverage the report is marked low confidence.

```
Old pod(E)    Controller     New pod(E+1)   Flink/Store
   |<- SIGTERM ---|               |              |
   | stop pacer   |               |              |
   |- - flush sec<=last_sec - - - - - - - - - - >|
   |              |-- lease(F) -->|              |
   |              |               |- - sec>=F - >|
   |- - zombie sec>=F (E) - - - - - - - - - - - >| reject
```

---

## Exchange 6 — Safe limits & kill switch

**INTERVIEWER:** The fencing and the ledger are good, but "local hard caps protect the target while guardrails are blind" only holds one run to its own plan. It does nothing to bound the total load on the target.

Here's the scenario. `payments-auth` in prod has an approved test ceiling of 30k RPS. Run A is at 18k and run B, from a different team, is at 15k. Each was approved on its own, and both span 3 regions. At minute 9, payments-auth p99 climbs from 120ms to 900ms and real checkouts start failing. Flink is mid-restore, so both guardrail evaluators are blind. On-call runs the kill CLI. It writes to us-east and eu-west etcd, but us-west's control plane is partitioned from the CLI. us-west agents can still reach their local etcd and keep renewing their 5s leases, and they're still sending about 11k RPS.

1. Who stops admitting 33k against a 30k ceiling, and where is that ceiling enforced at runtime across runs and regions?
2. What's your end-to-end kill latency budget, broken down by hop? What actually stops us-west, and how quickly?
3. Who is allowed to issue a kill, and how does an agent tell that a kill is authentic without the control plane? What stops a forged or replayed "resume"?

**CANDIDATE:** You're right, and there are two misses. Both the caps and the approvals were per run, so nothing ever owned the 30k ceiling for the target. And the dead-man lease only depended on the local etcd, so a partitioned region looks healthy to its own agents.

**1. Target budget as a first-class resource.** A global Budget Service runs on a 5-node Raft group spread across the 3 regions. It holds `target -> ceiling` and the live grants against it.
- **Admission:** a run reserves RPS transactionally. B asks for 15k when 18k is already reserved, so it gets rejected or capped at 12k.
- **Runtime:** each region holds a grant lease, `(target, run, region, rps, epoch)`, with a 10s TTL that it renews every 3s. Agent leases (5s) are now chained to that grant. If the region can't renew the grant, its controller zeroes all its shares, and agents also stop on their own once the grant's expiry passes. Prod fails closed.

**2. Kill path and latency.**
```
CLI --> Budget Svc (ceiling=0, quorum) ~0.3s
CLI --> regional etcd x3 (best effort)  ~0.5s
agent - - > global signed kill object, poll 1s
agent: stop pacer, RST in-flight        ~0.1s
```
In the normal case, load is off the target in ≤2s. In us-west, agents also poll a multi-region signed kill object every 1s, so they stop within about 2s even though their control plane is partitioned. If that path is down too, the grant TTL bounds it at 10–13s. There's a last, independent layer: every request carries a signed `X-Loadtest-Run` header, so payments-auth's mesh can shed all test traffic with one Envoy rule, in roughly 5–10s of config push. The target shouldn't have to trust us.

**3. Authority.** Kills are Ed25519-signed tokens `{scope, run_id|target, issued_at, nonce}`. The keys are held per on-call/owner role, and agents carry the public keys in their image. The bar to kill is low: target owners and on-call can do it, and a replayed kill is harmless because kills are idempotent. **There is no resume message.** A kill is a terminal tombstone that agents persist locally for that run_id. Restarting means a new run with re-approval and a fresh grant at a higher epoch, so a replayed old grant is rejected as `epoch ≤ seen`.

The part I'm unsure about is that this makes every prod test depend on a cross-region Raft group. I'd accept that for prod and let non-prod tests fail open to their local caps.

---

## Exchange 7 — Tradeoffs: what to cut for v1

**INTERVIEWER:** Calling out your own dependency on cross-region Raft is the right instinct, so let's push on it.

Here's the situation. You have a team of four engineers and one quarter to ship v1. Today the company runs about 20 load tests a week, and only a handful of them hit prod. Your design now includes per-second sharded pacing with epochs, Kafka with idempotent producers, Flink with keyed dedup state, an ownership ledger, a 5-node cross-region Raft Budget Service with chained grant leases, a multi-region signed kill object, Ed25519 key distribution, and Envoy shedding rules. Your skip-level asks: "Why does this need more consensus machinery than the services it's testing?"

1. Which of those components would you cut or defer for v1, and what simpler mechanism replaces each one? Be specific about the safety or correctness guarantee you lose with each cut and why that loss is acceptable at this scale.
2. Which one or two pieces would you refuse to cut even under that pressure, and why?
3. What concrete signal, whether usage, an incident, or a metric, would tell you it's time to build the deferred pieces?

**CANDIDATE:** The skip-level is right. I designed for 30 concurrent tests at 1M RPS, and we actually run about 3 a day. Here's v1:

| Cut | v1 replacement | Guarantee lost | Why OK now |
|---|---|---|---|
| Kafka + Flink | Agents PUT 1s HDR pieces to S3 keyed `(run, pod, sec)`; one aggregator polls every 5s | HA streaming, so guardrails go blind if the aggregator dies | ≤ ~200 pieces/s; dead aggregator = abort prod runs (below) |
| Epoch fencing / shard handoff | No rebalancing. A preempted pod's share is lost and reported as a hole. Prod runs get a non-preemptible priority class | ±5% rate during preemption | Coverage % still reported honestly |
| Raft Budget Service | Postgres `SELECT … FOR UPDATE` on the target row at admission; **one prod test per target at a time** | No runtime cross-run enforcement under partition | A handful of prod tests a week, so serializing costs nothing |
| Ed25519 / signed kill objects | Kill = row in the central API; mTLS + RBAC on the kill endpoint | Agents can't verify a kill offline | Kill is fail-safe anyway (below) |
| Ownership ledger | Expected pieces = pods × seconds from run metadata | Exact per-shard gap attribution | Coverage % is enough |

**Won't cut:**
1. **Fail-closed dead-man lease against the *central* API**, plus a local hard RPS cap. If an agent can't renew in 10s, it stops. That's the one mechanism that bounds harm to payments-auth when anything else breaks, and it's about 100 lines. Tagging every request with `X-Loadtest-Run` costs a day, so it stays too: it gives target owners their own off-switch.
2. **Correct measurement**: intended-time pacing, censored slots recorded at 5s, bucket-wise HDR merge. If we cut those, the tool produces confident wrong numbers, and that's worse than having no tool.

**Triggers:**
- Kafka/Flink when concurrent runs exceed ~10, or the aggregator's p95 lag goes over 10s.
- Budget service when the prod-test queue wait for any one target goes over a day, or any incident shows combined test load breaching a ceiling.
- Epoch handoff when more than 5% of runs end below 99.5% coverage.
- Signed kills when a quarterly kill drill takes more than 10s, or when usage spreads beyond owners and on-call.

---

## Exchange 8 — Fleet-level bottleneck isolation

**INTERVIEWER:** That's a defensible v1. One last question.

Your first big prod test targets payments-auth at 300k RPS over HTTPS. The agent pods run in a private subnet and all reach the target's public endpoint through a shared NAT gateway. At around 180k RPS, p99 climbs from 40ms to 900ms, connection errors appear, and the target team says their dashboards look flat: normal CPU, normal p99 at their load balancer. Your per-agent CPU self-checks are all green.

1. Walk me through which layers between your pacer and their LB could be the actual bottleneck. Be concrete about the specific limits involved.
2. What would your system need to measure or report so that a run like this gets flagged as "generator-limited, results invalid" automatically, rather than someone filing a P1 against payments-auth?
3. What would you change in the v1 deployment so this doesn't happen in the first place? Keep in mind the constraints you set last turn.

**CANDIDATE:** The target's LB is flat, so the problem is almost certainly on our side of it. From experience, the suspect is connection setup, not request processing.

```
pacer --> conn pool/TLS --> pod netns --> node conntrack/SNAT --> NAT gw --> internet --> target LB
```

**1. Candidate layers and their limits** (from memory, please verify the exact numbers):
- **Pool behavior:** if keep-alive is off, or idle connections get reaped, every request pays a TCP and TLS handshake. That kills the ports and CPU on everything downstream of us.
- **Per-pod ephemeral ports:** the default range is about 28k, and TIME_WAIT lasts 60s. At ~470 new conns/s a pod runs out of ports and gets `EADDRNOTAVAIL`.
- **Node conntrack:** `nf_conntrack_max` is often 128–256k per node. When it fills, SYNs get dropped silently and the retransmit backs off by 1s, which lines up with p99 jumping to ~900ms.
- **NAT gateway:** this is my top suspect. AWS allows about 55k concurrent connections per NAT IP for each destination IP:port. GCP Cloud NAT defaults to only 64 ports per VM. With 3–6 LB IPs and a single NAT IP, the ceiling is around 200–300k flows. Under churn we hit it, and the target never sees the dropped SYNs.
- **The LB itself:** all of our traffic arrives from one source IP, so per-source rate limits or a WAF can also throttle it.

**2. Automatic "generator-limited" flag.**
- Split each request into its phases with httptrace: DNS, connect, TLS, TTFB.
- Count connect errors by errno.
- Track the connection reuse ratio and new connections/s per pod.
- Collect node conntrack `insert_failed` and the NAT gateway's drop and port-allocation metrics.
- At ingest, cross-check our sent RPS against the target LB's request count.

Mark the run invalid when the latency growth is in the connect/TLS phases, TTFB is flat, connect errors are non-zero, and the LB sees ≥5% less traffic than we sent.

**3. v1 deployment changes.**
- Prod agents get a dedicated egress path:
  - Preferred: private connectivity to the target's internal LB, with no NAT.
  - Otherwise: a dedicated NAT with N IPs, sized at admission as connections ÷ 50k.
- Keep-alive pools are fixed, prewarmed and capped, and new connections/s is capped.
- `ip_local_port_range` and conntrack sizes are raised.
- At every mandatory ramp step, the ramp holds unless the cross-check passes.

None of this needs new consensus.

---

## Exchange 9 — Close

**INTERVIEWER:** ENDING: Okay, let's stop there. We're at time, and we covered everything I wanted to get through today. Thanks for walking me through the design in this much depth. We have a minute left, so do you have any questions for me about the team, the work, or the process from here?

---

# Retrospective (critical staff-level observer)

**1. What the candidate did well**
- **Measurement was precise.** In exchange 3 they split each request into three timings: `response_latency` (done − intended), `service_latency` (done − socket write) and `send_lag`. That gives the "generator-suspect" timeline lane, which directly answers "our stall vs. the target's degradation." In exchange 4 they recorded censored slots at 5s, showing they took the interviewer's point on board.
- **The pipeline reasoning held up.** They said "Two copies the producer already wrote are two distinct offsets, so Flink counts both correctly, twice." The dedup key `(run_id, shard_id, epoch, sec)` leaves the pod out, and zombie writes are fenced at second F.
- **Their v1 cut was honest.** In exchange 7 the table lists what each cut loses, keeps a fail-closed dead-man lease plus correct measurement, and names concrete triggers for building the deferred pieces.

**2. What a critical reviewer would flag**
- **The first design was over-engineered.** In exchange 2 they reached for Postgres, a scheduler, k8s operators, etcd, Kafka, Flink, a TSDB and S3. By exchange 6 a Raft group, Ed25519 and Envoy rules were added on top. They only simplified when the interviewer forced it. A senior candidate should open with the v1 and only then show how it scales.
- **Pacing doesn't fit a real 45 minutes.** Eleven scoping questions, plus derived bucket widths, DDSketch bucket counts, sequence diagrams and cloud NAT port limits, is more than 60 minutes of talking. Nobody recites `ln(16,667)/0.01` live, and they shouldn't try.
- **Some numbers don't hold up:**
  - Exchange 3 allows up to 10k HTTP/1.1 sockets per pod. Across 200 pods that is about 2M connections, which blows past the roughly 55k-per-destination NAT limit they cite in exchange 8. Nobody connected the two.
  - The 10k in-flight cap equals Little's law at 2s exactly, so there is no headroom.
  - "45 + 15 missing pieces" doesn't match three unflushed agents.
  - Several topics were missed: clock skew between pods (pieces are keyed by intended-send second across regions), how agents spread across the target's LB IPs and DNS, and cost and quota on the shared pool.

**3. Where the interviewer could have pushed harder**
- The interviewer gave contradictory scale: "30 concurrent tests" in exchange 2, then "20 tests a week" in exchange 7. The candidate should have caught this. The interviewer should have tested whether they would.
- The candidate flagged two open doubts: the 2x catch-up cap, and where the "multi-region signed kill object" lives (itself a new dependency). The interviewer let both pass and never forced a decision.

**4. Takeaways for practicing at senior level**
- **Scoping (about 5 min):** pin down peak RPS, how many tests run at once, prod versus non-prod, and accuracy targets. Then design the v1 first: a central API and Postgres, agents with a local pacer, histograms written to blob storage, and one aggregator.
- **Must-hit points:**
  - *Paced agents:* schedule by intended time, and keep `send_lag` separate from latency.
  - *Latency histograms:* mergeable HDR or DDSketch, and never average percentiles.
  - *Result ingestion:* idempotent keys plus a coverage percentage.
- **Safe limits:** have a per-target ceiling across all runs, not only per run. Add a fail-closed lease, a local hard cap, and a request tag the target team can shed on.
- **Bottleneck isolation:** know the chain conn pool → ephemeral ports → conntrack → NAT → LB, and cross-check your sent count against the target LB's count.

---

**Next step:** `/system-design mock --level=senior Design a distributed load-generation and measurement service`. Answer the question yourself under scoring. Aim to open with the simple v1 design and get through all six guidance areas in about 40 minutes.
