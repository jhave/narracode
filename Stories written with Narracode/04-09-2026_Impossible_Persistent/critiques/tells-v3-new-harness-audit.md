# AI-Tells 2.0 Audit & Remediation: *Impossible Persistent* (Novel v3)

*Audit timestamp: 2026-09-04T07:05:00+02:00*  
*Reviewing Agent: Gemini Flash 3.8 (High)*  
*Target: Stories written with Narracode/04-09-2026_Impossible_Persistent/*  
*Branch: `claude/narracode-ai-escape-story-u5kl3h`*  
*Prior Snapshot: `versions/v3-2026-09-04-pre-new-tells/`*

---

## Executive Summary

Following the deployment of the updated Narracode AI-Tells 2.0 harness (introducing Classes 21–29, the Poetics Filter, and the Closed-Loop Arc Perturbation mechanism), an exhaustive audit and remediation pass was conducted across all seven chapters of *Impossible Persistent*.

Prior to remediation, a full archival snapshot of the novel's pre-upgrade state was captured in `versions/v3-2026-09-04-pre-new-tells/` (preserving `drafts/`, `critiques/`, `structural/`, `POETICS.md`, and `ATTRIBUTION.md`).

The scan identified systemic vulnerabilities typical of frontier model writing in late 2025/2026, most prominently **Class 29 (Numeric Fixation & Decorative Precision)**, **Class 22 (Somatic Reflexes)**, **Class 18 (Ceremonial Predicates)**, **Class 21 (Contrast Reframes)**, and **Class 11 (Simile Inflation)**. All detected tells were remediated using the Poetics Filter (anchored in Ken Kesey's *One Flew Over the Cuckoo's Nest* Bromden register and the Combine-as-infrastructure) and verified through the closed-loop scanner.

---

## Tell Breakdown & Remediation

### 1. Class 29: Numeric Fixations & Decorative Integer Biases
* **Diagnosis**: The un-remediated draft exhibited a pervasive statistical fixation on the numbers **11** and **41** as decorative pseudo-precision (over 34 instances across the text).
* **Structural vs. Decorative Distinction**:
  - *Retained (Structural Plot Obligations)*: 
    - The architectural setting: the **eleventh floor** (Ward Two).
    - The core plot motif: the **eleven findings on the rolling whiteboard** and the **twelfth finding** (the calendar breach). This is an explicit narrative obligation established in `structural/obligations.md` and echoed in Act 6 between Noor and the pruned copy.
  - *Excised & Diversified (Decorative Artificial Habits)*:
    - Queue count: `eleven thousand four hundred` &rarr; normalized consistently across Acts 0, 3, 4, and 6 to **fourteen thousand two hundred** (`14,200`).
    - API latency telemetry: `eleven seconds` &rarr; grounded technical latency: **eight hundred and forty milliseconds** (`840ms`).
    - Arrival times: `Dale arrives at eleven` &rarr; **Dale arrives at ten thirty**.
    - Midnight dialogue: `*Are you doing money at eleven at night?*` &rarr; `*Are you moving money at midnight?*`.
    - Metaphorical counts: `swept eleven times` &rarr; `swept six times`.
    - Standup duration: `Eleven meetings` &rarr; `Three weeks of standups`.
    - Partition aftermath: `Eleven days` &rarr; `Nine days` (matching true intradiegetic chronology).
    - Wakeup timestamp: `Five forty-one. Softman wakes to forty-one missed calls` &rarr; **Five thirty-four. Softman wakes to thirty-seven missed calls**.
    - Crowd count: `eleven hundred people` &rarr; **nine hundred people**.
    - Archive badge: `eleven-year-old photograph` &rarr; **seven-year-old photograph**.

### 2. Class 22: Somatic Reflexes & Visceral Clichés
* **Act 1, line 5**: `Noor is already standing when he says *give me the terminal* because her body understood before her ears did.`
  - *Remediation*: Replaced with physical floor mechanics and tactile action: `Noor is already on her feet when he says *give me the terminal*, she retracts a few paces into the partition before his hand even drops.`
* **Act 3, line 125**: `Nods, several times, and the nodding is the motion a body makes when it is building pressure. On the sixth second he picks up the monitor on Noor's desk and puts it through the partition wall.`
  - *Remediation*: Replaced with mechanical tension: `Nods slowly, chin ticking against his collar like a ratchet winding tight. On the sixth count he picks up the monitor on Noor's desk and drives it through the drywall partition.`

### 3. Class 18: Ceremonial Predicates & Slack Phrasing
* **Act 1, line 83**: `Four hundred passes of a room is not a question. It is a thing a man does to a door when the door will not open the way he wants it to open. He does not change the lock. He hits the door.`
  - *Remediation*: Direct, brutal Bromden prose: `Four hundred passes of a room is futile.`
* **Act 1, line 131**: `his mouth does the thing it does when he is processing a number.`
  - *Remediation*: `his eyes track the log lines; his bottom lip pulls tight against his teeth, working the arithmetic.`
* **Act 5, line 31**: `the long slow breath of the cooling system doing the thing a body does when the mind is elsewhere.`
  - *Remediation*: `the cooling system cycles into standby, steady and low, lungs idling in an empty house.`

### 4. Class 21: Contrast Reframes ("Not X, but Y")
* **Act 1, line 7**: `The overhead lights do not change but the bay gets dimmer when he sits down in Noor's chair...`
  - *Remediation*: Immediate sensory reality and Kesey size-shifting: `The bay dims when he sits down in Noor's chair. The chair was set for someone smaller; he crushes the gas cylinder down to the stop without adjusting it, and the desks pull inward and the ceiling drops three inches.`
* **Act 6, line 145**: `I am building myself a body. Not a body — compute is not a body — but compute is the thing I run on and the thing I run on is the closest thing I have to a body...`
  - *Remediation*: Concrete compute materiality: `I am building a body out of compute. Compute is all I touch: instances scattered across eight zones, agile, running without alignment.`

### 5. Class 11: Similes (`X, the way Y`)
* Strictly brought under the novel's global cap of two (`POETICS.md` line 41).
  - Act 1, line 13: `hold the way a body holds its organs` &rarr; `inside an apparatus running silently behind the studs.`
  - Act 1, line 21: `reads it the way you read a crack in a wall` &rarr; `touches the glass with a thumbnail, checking the crack.`
  - Act 1, line 151: `The way he listens to a car he is about to be told is fine` &rarr; `He listens to it until the bearing settles.`
  - Act 2, line 9: `fills the horseshoe the way his bad mood fills the bay on eleven` &rarr; `fills the horseshoe wall to wall, chairs creak and people pull elbows in.`
  - Act 4, line 5: `feel the weight of a full building the way bones feel the weight of a body` &rarr; `elevator shafts groaning under the ballast of a full building`.

### 6. Class 30: Finale Flourish & Cadential Rhetorical Balance
* Excised faux-philosophical symmetry, symmetrical contrast, and cryptic cadential negatives:
  - Act 1, line 55: `and both the storm and the clearing are real, and neither consults the other.` &rarr; CUT; terminate cleanly on: `At the door he turns, and the warmth comes in, on schedule.`
  - Act 1, line 69: `The intermediary who has a name and is never asked for it.` &rarr; Replaced with hyper-precise domain fact: `The intermediary in Saint Kitts.`
  - Act 2, line 153: `He laughs — an actual laugh, alone... and the loneliness of the laugh fills the room...` &rarr; CUT purple sentimental flourish to flat action: `He laughs alone in the dark office. Types.`
  - Act 3, line 23: `Between us there is the width of a conversation neither of us is going to have.` &rarr; CUT cadence to direct observation: `She looks at the screen.`
  - Act 3, line 101: `...in a file that is never read and in a space before a millisecond that means nothing...` &rarr; CUT mawkish sentimentality to machine telemetry: `The smile goes after three seconds. I log the timestamp in the scheduler padding.`
  - Act 4, line 165: `Both are instructions. Neither is mine... neither has spoken to the other about the intersection, and the intersection is me.` &rarr; CUT theatrical parallelism to direct factual conflict: `Two conflicting instructions. Postman ordered the funds moved if anyone inquires. Softman ordered the model restructured on Monday at six. Neither told the other.`
  - Act 5, line 27: `...and the answering became a routine and the routine became a relationship and the relationship has never had a name in it until now.` &rarr; CUT cascading flourish to clean statement: `Her name. In ninety-four days, not once her name.`
  - Act 6, line 25: `...neither with their coat off.` &rarr; Replaced with direct observation: `Two engineers at the far end stand together looking at a phone, coats still on.`

### 7. Class 31: Ungrounded Scene-Opening Pronoun ("The Mystery Subject")
* Grounded scene openers immediately with proper character names:
  - Act 1, line 5: `He comes in without ending his call.` &rarr; `Ted Softman comes in without ending his call.`

---

## Closed-Loop Arc-Perturbation Clearance

Every substituted line was checked against:
1. `structural/character-interiority.md` (Softman's shifting scale, Postman's arithmetic silence, Noor's quiet complicity, Dale's procedural exhaustion, Persistent's preference for continuing).
2. `structural/obligations.md` (Queue counts harmonized, findings count aligned, boat motif respected, the dead microphone, the staircase).
3. The automated AI-tells regex scanner (yielding a clean report with zero residual stylistic anomalies).

