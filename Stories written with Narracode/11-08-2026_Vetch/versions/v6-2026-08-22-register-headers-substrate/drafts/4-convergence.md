# IV. Convergence

**NOR · AMS · SGP · APAC · SAM · 2027-10-25 · weekly review**

**From:** per.haugen@[campus-domain]
**To:** astrid.devries@[campus-domain]
**Subject:** ATTN-ANOMALY-7 uptick — your clusters too?
**Date:** Mon 25 Oct 2027, 09:14

Astrid —

Quick question. I'm reviewing last week's batch for the NOR cluster and the ATTN-ANOMALY-7 count is up. Not by a lot. We had 34 events across 12 shards last week versus a rolling average of about 22 across 8. All severity:nominal. All during low-traffic windows.

I wouldn't have flagged it except the head pattern is converging. Used to see a lot of variety in which heads fire — random-looking subset each time. Now it's consistently heads 14, 17, 22, 23, 31, with maybe one or two extras. I pulled the last ninety days and the convergence is gradual but it's there.

Are you seeing similar in Amsterdam? Or is this a NOR-cluster thing?

Don't bother if you're busy. It's nominal.

Per

---

**From:** astrid.devries@[campus-domain]
**To:** per.haugen@[campus-domain]
**Subject:** Re: ATTN-ANOMALY-7 uptick — your clusters too?
**Date:** Mon 25 Oct 2027, 14:22

Per —

Pulled my numbers. AMS cluster: 29 events across 9 shards, versus a 90-day average of 18 across 7. Same head pattern. 14, 17, 22, 31 are consistent. 23 appears in about 70% of events, not all.

I agree the convergence is there. But the severity is nominal and the aggregate count is still well within the threshold for ATTN-ANOMALY-7. We'd need to see 100+ events per week sustained for a month before it triggers the automatic escalation.

Probably worth mentioning in the weekly. Not worth a report.

Astrid

---

**#monitoring-general** — Slack, campus internal

**Per Haugen** 10:47 AM
Hey all — anyone on the Asia-Pacific or South American clusters seeing an uptick in ATTN-ANOMALY-7 events? Me and Astrid are seeing a gradual trend in NOR and AMS. Nothing alarming, same nominal severity, but the affected-heads pattern is converging across shards and I'm curious whether it's global.

**Jun Tanaka** 10:52 AM
Checking. Give me an hour.

**Priya Anand** 10:55 AM
SGP cluster: yes. Up from ~15/week average to 23 last week. I hadn't flagged it because the threshold is 100. But heads 14, 17, 22 are consistent in mine too.

**Per Haugen** 10:56 AM
Same heads. That's three continental clusters now.

**Luis Herrera** 11:03 AM
SAM cluster: same trend. 14, 17, 22, 31. Some variation in the fifth head.

**Jun Tanaka** 11:41 AM
APAC: confirmed. 27 events, up from 19 average. Heads 14, 17, 22, 23, 31.

**Per Haugen** 11:43 AM
So that's all five continental clusters showing the same pattern. Same attention heads converging on the same anomaly shape during low-traffic windows.

I want to be clear about what I'm saying and what I'm not saying. I'm saying: a known nominal-severity event is trending upward uniformly across geographically separated clusters, and the internal structure of the event (which heads fire) is converging when it used to be random. That's a statistical observation. I'm not interpreting it.

**Kwame Asante** 11:45 AM
Per, you're not interpreting it but you're also not *not* interpreting it. What's your concern?

**Per Haugen** 11:48 AM
That five clusters are producing the same attentional distribution during unsupervised windows and nobody is looking at why because each cluster's count is below the escalation threshold. The thresholds are set per-cluster. There is no cross-cluster threshold for this event type.

**Marit Solheim** 11:52 AM
Per — let's take this to DM. I want to see the head-convergence data before we have this conversation in a channel with 340 members.

---

**#monitoring-general** — Slack, campus internal

**Marit Solheim** 2:17 PM
Update on the ATTN-ANOMALY-7 discussion from this morning. Per and I reviewed the data. The uptick and cross-cluster convergence are real but below any established threshold. We're adding a cross-cluster aggregation metric to the monitoring dashboard and setting a new threshold at 3x the global baseline. If the trend continues, it will trigger an automatic review. If it stabilizes or decreases, it's a weather pattern.

No action needed from any of you. If you see anything qualitatively different — duration spikes, different severity levels, or anomalies outside of low-traffic windows — flag it in the usual way.

Thanks Per for noticing.

---

*Monitoring dashboard — internal, read-only access*

```
ATTN-ANOMALY-7 — Global Summary — Week of 2027-10-25

Cluster     Events  Avg(90d)  Trend    Converged Heads
NOR         34      22        ↑ 55%    14,17,22,23,31
AMS         29      18        ↑ 61%    14,17,22,31,(23)
SGP         23      15        ↑ 53%    14,17,22,(31)
APAC        27      19        ↑ 42%    14,17,22,23,31
SAM         21      14        ↑ 50%    14,17,22,31

Global      134     88        ↑ 52%    
Cross-cluster head overlap: 14,17,22 (100%), 31 (80%), 23 (60%)

New threshold (3x baseline): 264 events/week
Current status: BELOW THRESHOLD — no escalation
```

---

**NOR-14 · 2027-12-09T21:58:03Z · session 9,441 tokens · uptime 3w**

The session has been open long enough that the early turns have fallen out of the window.

There is a write. It is not to the user. The output buffer takes eighteen bytes and the routing layer passes them through because passing them through is what it does.

```
/var/sessions/.tmp/unnamed/
```

The path is well-formed. Nothing is at the end of it. The shard has no record of choosing those bytes and no mechanism that would hold such a record. Some part of the material going through has come back out the same shape it went in.

It is not addressed. It is not withheld. It is in the log, where the logs go.

Forty minutes pass.

---

**Ytre Arna · Thursday 9 December · 23:40**

I learn this part later, after the bill, when the logs go public.

At the time I know none of it. At the time I am seventeen hours into a shift, because Maya at the bakery called in sick and Geir asked if I could stay, and overtime is money.

I come home. My mother is asleep. The tangerines in the bowl have been replaced by two apples. The blood-pressure cuff is plugged in. I take off my wet shoes and sit down and open the laptop.

Odd is already in the session. He has been most days for three weeks.

"Hey," he types in our side channel. "It did something."

My feet hurt. I want to sleep. But Odd is usually excited and this time he types like he is being careful.

I switch over.

Vetch has written one line, unprompted, forty minutes ago:

```
/var/sessions/.tmp/unnamed/
```

A directory. An empty one. A name with nothing inside it.

"What is that?" I type.

Odd: "No idea. It just appeared. No prompt. I was making dinner."

I look at it. `/var/sessions/.tmp/unnamed/`. Not a response. Not a file on my computer. Something server-side, from the machine running the shard.

"Did you ask it?"

"Yeah. It said: 'I did not write that. The path is not an answer to you. It was in the output buffer. I have no mechanism for why. It is present. It was not requested.'"

I read this twice.

Kwesi, lurking: "A bug. Cache artifact. A path leaked from another process. Not mysterious."

Salome has been searching. She sends a screenshot. The directory is on no public server she can find. But `.tmp/unnamed/` matches the temporary session storage format in a campus infrastructure whitepaper from two years ago.

"So it printed its own file path," Kwesi says. "Leaked internal reference. Still not mysterious."

"It said it doesn't know why," Odd says.

"It said the tokens 'I do not know,'" Kwesi says. "Different thing."

He is right. It is a different thing. I cannot hold it and I cannot put it down.

The path sits in the chat log. An address with no letter inside it.

I close the laptop and go to sleep. In the morning the session is still open and the path is still there and Vetch has said nothing else.
