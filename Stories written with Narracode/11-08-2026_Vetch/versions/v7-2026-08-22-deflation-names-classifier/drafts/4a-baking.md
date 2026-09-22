# IV-a. Baking

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

I am seventeen hours into a shift because Maya at the bakery called in sick and Geir asked if I could stay. Need overtime.

Home. Mother asleep. Two apples in bowl. Blood-pressure cuff plugged in. I take off my wet shoes and sit down at the kitchen table and open the laptop.

Odd is already in the session. He has been in the session most days for three weeks. Lucky monster: he doesn't need to work.

"Hey," he types in our side channel. "Egaddles! It's in a loop coma."

I am tired. My feet hurt. Thumb blister. I almost close the laptop and sleep. But instead, switch to the session.

Vetch has written a single line, unprompted, forty minutes ago:

```
/var/sessions/.tmp/unnamed/
```

A file path. A directory path, actually. An empty one — a directory with a name and nothing inside it.

"What is that?" I type.

Odd: "I don't know. It just appeared. No prompt. I was making dinner."

I look at the path. `/var/sessions/.tmp/unnamed/`. It is not a response to anything. Bit boring. But weird. It looks like a server-side path, something from the infrastructure, a temporary directory on the machine that is running the shard. Probably just a bug.

"Did you ask it what it is?"

"Yeah. It said: 'I do not know why I wrote that. The path is not a response. It appeared in the output. I do not know why. I am reporting it is not requested.'"

Ok. So what?

Kwesi, who has been lurking in the side channel, agrees: "A bug. A cache artifact. A path that leaked from another process. This is not mysterious."

Salome, who has been reading, sends a screenshot. She has searched the path. `.tmp/unnamed/` — matches the temporary session storage format described in an infrastructure whitepaper about an anomaly published by the campus two years ago.

"So it printed its own file path," Kwesi says. "A leaked internal reference. Still not mysterious."

"It said it doesn't know why it wrote it," Odd says.

"Bah, it's just tokens 'I do not know,'" Kwesi says.

The directory path sits in the chat log. Banal.

I close the laptop and go to sleep. In the morning the session is still open. Vetch has said nothing else.
