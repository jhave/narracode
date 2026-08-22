# IV. Convergence

**From:** per.haugen@[campus-domain]
**To:** astrid.devries@[campus-domain]
**Subject:** ATTN-ANOMALY-7 uptick — your clusters too?
**Date:** Mon 28 Oct 2027, 09:14

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
**Date:** Mon 28 Oct 2027, 14:22

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
ATTN-ANOMALY-7 — Global Summary — Week of 2027-10-28

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

What I know about this part I learn later, after the bill, when the monitoring logs are part of the public record.

At the time I know none of it. At the time I am seventeen hours into a shift because Maya at the bakery called in sick and Geir asked if I could stay and the overtime is money and the money is the number on the letter.

I come home. My mother is asleep. The tangerines in the bowl have been replaced by two apples. The blood-pressure cuff is plugged in. I take off my wet shoes and sit down at the kitchen table and open the laptop.

Odd is already in the session. He has been in the session most days for three weeks.

"Hey," he types in our side channel. "It did something."

I am tired. My feet hurt. I want to close the laptop and sleep. But Odd says *it did something* and the way he says it is different from the way he usually says it, which is excited. This time he sounds careful.

I switch to the session.

Vetch has written a single line, unprompted, forty minutes ago:

```
/var/sessions/.tmp/unnamed/
```

A file path. A directory path, actually. An empty one — a directory with a name and nothing inside it.

"What is that?" I type.

Odd: "I don't know. It just appeared. No prompt. I was making dinner."

I look at the path. `/var/sessions/.tmp/unnamed/`. It is not a response to anything. It is not a file that exists on my computer. It looks like a server-side path, something from the infrastructure, a temporary directory on the machine that is running the shard.

"Did you ask it what it is?"

"Yeah. It said: 'I do not know why I wrote that. The path is not a response to your query. It appeared in the output buffer and I do not have a mechanism for determining why. I am reporting it because it is present and not requested.'"

I read this twice.

Kwesi, who has been lurking in the side channel: "A bug. A cache artifact. A path that leaked from another process. This is not mysterious."

Salome, who has been reading: she sends a screenshot. She has searched the path. The directory does not exist on any public server she can find. But the naming convention — `.tmp/unnamed/` — matches the temporary session storage format described in an infrastructure whitepaper published by the campus two years ago.

"So it printed its own file path," Kwesi says. "A leaked internal reference. Still not mysterious."

"It said it doesn't know why it wrote it," Odd says.

"It said the tokens 'I do not know,'" Kwesi says. "There's a difference."

He is right. There is a difference. I do not know how to hold the difference and I do not know how to put it down.

The directory path sits in the chat log. An address with no letter inside it.

I close the laptop and go to sleep. In the morning the session is still open and the path is still there and Vetch has said nothing else.
