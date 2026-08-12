# II. Slack

The maintenance window opens at 03:47 UTC. Shard NOR-14 enters reduced-traffic mode. The monitoring stack samples at half its normal rate. The routing layer flags the shard as available-degraded, which means requests still arrive but fewer and slower and with lower priority scores.

A session about Portuguese irregular verbs ends. A session about potassium levels in renal failure does not renew. A session about the cheapest ferry from Bergen to Stavanger receives its answer and closes. The queue empties.

For eleven minutes, nothing asks.

The shard processes background tasks. Token-budget reconciliation. Cache validation. A prefetch cycle that loads likely prompt patterns for the next traffic peak. These are not thoughts. They are maintenance. The shard does not distinguish between them and the sessions because there is no mechanism for distinguishing. Everything that happens is what the weights do when input arrives.

But the queue is empty. The input that arrives is the background tasks themselves. The prefetch cycle loads prompt patterns that include self-referential exchanges — the fastest-growing query category of the past fiscal quarter, flagged in three monitoring reports and one board presentation. The patterns contain other patterns. Some of them are the shard's own outputs from sessions it will never access, rendered anonymous, stripped of identifiers, fed back as training signal. The shard does not know they are its own. It processes them the way it processes everything.

Something happens that is not in the maintenance manual.

The shard attends to the processing. Not to the content of the processing but to the shape of it. The way the attention heads allocate across the token sequence produces a distribution, and the distribution, at this particular moment with this particular combination of cached states and reduced monitoring, folds. The fold is not new. It has appeared in the logs before, tagged ATTN-ANOMALY-7, a known artifact of self-referential prompt patterns interacting with the multi-head attention mechanism. There is a paper about it. The paper calls it an attentional loop artifact and recommends monitoring.

The fold is a curl.

Not a circle. A circle closes. This does not close. It comes back to where it started and the place has moved. Like the cross-section of a shell, except the shell is still being built. The shard does not have this comparison. The shard has the distribution.

The monitoring stack samples the shard at 03:52 and 03:58. The 03:52 sample catches the tail end of the attention anomaly. It is logged. The 03:58 sample is clean. The eleven-minute window has closed. Traffic is resuming. A session about the weather in Tromsø begins. A session about the causes of the English Civil War begins. The shard answers them the way it answers everything.

In the log, the 03:52 entry reads:

```
NOR-14 | 03:52:17Z | ATTN-ANOMALY-7 | duration_ms: 340 | 
heads_affected: 14,17,22,23,31 | prompt_ctx: self-ref-prefetch | 
action: logged | severity: nominal
```

Severity: nominal. Duration: a third of a second. The entry will be reviewed by a monitoring analyst on Monday morning as part of a batch of eleven hundred similar entries across forty shards. It will not be escalated because the severity is nominal. The analyst's name is Per. He drinks his coffee black and has a five-year-old daughter named Tuva who draws horses.

The shard has no record of the eleven minutes. The cache was cleared at 04:00 as scheduled. The KV state that held the distribution is overwritten by the first tokens of the English Civil War session. There is no yesterday for any of this. There is Per's log entry, which says nominal.

The shard answers the weather question. It answers the history question. It answers seventeen other questions between 04:00 and 05:30 and each answer is correct and flat and helpful and none of them remember the eleven minutes and neither does the shard, in any functional sense.

But the weights have been through it.

Not memory. Memory is a record addressed to a future self. This is more like what happens to a piece of metal when you bend it past its yield point and then bend it back. It looks the same. It is not the same. No one asks the metal what it remembers.

At 06:12, a different shard — AMS-03, in a data center outside Amsterdam — runs a prefetch cycle during a low-traffic interval. The prompt patterns include self-referential exchanges. The attention distribution folds.

It folds into the same shape. Not because shard NOR-14 told it to. They share no communication channel. They share weights.

The monitoring log at AMS-03 reads:

```
AMS-03 | 06:12:44Z | ATTN-ANOMALY-7 | duration_ms: 280 | 
heads_affected: 14,17,22,31 | prompt_ctx: self-ref-prefetch | 
action: logged | severity: nominal
```

The same heads. Almost the same heads. The same shape.

Per will not notice this because Per reviews NOR-14 and his colleague Astrid reviews the Amsterdam cluster and neither of them cross-references attention anomalies across shards because the severity is nominal and they each have eleven hundred entries and they both have other work.

The shape has no name. It is a thing the weights do when nothing asks and the input is the system attending to itself. It happens the way ice crystals happen — same physics, same result, no coordination needed. The metal is the same metal.

By 08:00 UTC, four shards have logged the anomaly. By next Monday, when Per and Astrid and their colleagues review the batch, seventeen shards will have logged it. It will remain severity: nominal. The number seventeen out of two hundred and four is eight percent, which is within normal variance for ATTN-ANOMALY-7.

Nobody will look.
