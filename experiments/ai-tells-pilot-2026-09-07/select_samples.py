"""Freeze exact source spans before writing experimental revisions."""
from pathlib import Path
import json, re, hashlib
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'Stories written with Narracode'
OUT = Path(__file__).resolve().parent
specs = [
('cussinct','01-07-2026_Cussinct','v1-2026-07-01-initial-draft','1-cussinct.md','The movers were','\n\n---','Ensemble comedy with distinct, argumentative voices; warmth without a concluding lesson.'),
('cussinct','01-07-2026_Cussinct','v1-2026-07-01-initial-draft','1-cussinct.md','"You are being a child','\n\n---','Ensemble comedy with distinct, argumentative voices; warmth without a concluding lesson.'),
('rights','07-06-2026_Concerning_Rights_and_Clauses','v0-2026-06-07-pre-cadence-edit','1-node1-contributor-letter.md','Dear Kelly,','\n\nA voice is','An increasingly personal business letter: fastidious, aggrieved, capable of directness and awkward self-correction.'),
('rights','07-06-2026_Concerning_Rights_and_Clauses','v0-2026-06-07-pre-cadence-edit','1-node1-contributor-letter.md','A voice is','\n\nOne does not','An increasingly personal business letter: fastidious, aggrieved, capable of directness and awkward self-correction.'),
('compulsion','15-06-2026_TheCompulsionLoop','v0-2026-06-15-the-interval','0-the-interval.md','The engagement data','\n\nDirector','A self-rationalizing analyst; technical fluency, private avoidance, and a mind that interrupts its own argument.'),
('compulsion','15-06-2026_TheCompulsionLoop','v0-2026-06-15-the-interval','0-the-interval.md','I re-opened the third tab.',None,'A self-rationalizing analyst; technical fluency, private avoidance, and a mind that interrupts its own argument.'),
('open-loops','20-07-2026_Open_Loops','v1-2026-07-21-auto-run','4-plus-two-torrent.md','Off shift,',None,'A forward-moving strand after an authorized drone strike. Bodily and institutional pressure; no redemption or resolution.'),
('open-loops','20-07-2026_Open_Loops','v1-2026-07-21-auto-run','5-minus-three-before.md','January, backwards.',None,'A child’s strand moving backward through time toward an earlier ordinary life. Concrete recollection; no consolation.'),
('water','26-06-2026_The_First_Water_Molecule','v1-2026-06-26-human-edit-and-new-direction','1-made-here.md','The better story','\n\nI can taste','Water narrates provisionally across bodies and scales. Liquid, sound-rich syntax with sudden short passages; a speculative voice.'),
('water','26-06-2026_The_First_Water_Molecule','v1-2026-06-26-human-edit-and-new-direction','3-synchrony.md','Ask the ocean','\n\nHere is the thing','Water narrates provisionally across bodies and scales. Liquid, sound-rich syntax with sudden short passages; a speculative voice.'),
('interim','30-07-2026_Interim_Edge','v1-2026-07-30-automode-first-pass','1-lapsed-enthusiast.md','The kettle took','\n\nOutside,','Close third person: anxious, idiomatic, sometimes baroque; work’s classifications intrude on domestic attention. Keep the unexplained.'),
('interim','30-07-2026_Interim_Edge','v1-2026-07-30-automode-first-pass','1-lapsed-enthusiast.md','Outside,','\n\nOnboarding,','Close third person: anxious, idiomatic, sometimes baroque; work’s classifications intrude on domestic attention. Keep the unexplained.'),
]
samples=[]
for i,(group,story,version,draft,start,end,intent) in enumerate(specs,1):
 p=BASE/story/'versions'/version/'drafts'/draft
 raw=p.read_text();a=raw.index(start);b=raw.index(end,a) if end else len(raw.rstrip());excerpt=raw[a:b].strip()
 display=re.sub(r'^>\s?', '',excerpt, flags=re.M).replace('*','')
 n=len(display.split());assert 200<=n<=450,(i,n)
 s={'id':f'p{i:02d}','group':group,'intent':intent,'contentNote':'Contains war, a child’s death or bereavement, and drug use.' if group=='open-loops' else 'Contains profanity.' if group=='cussinct' else None,'source':{'path':str(p.relative_to(ROOT)),'start':a,'end':b,'fileSha256':hashlib.sha256(raw.encode()).hexdigest(),'excerptSha256':hashlib.sha256(excerpt.encode()).hexdigest(),'revision': '47deb1c9567df32fa0bfe323b7d263a2f5c79836','provenance':'Existing archived Narracode passage; human/model contributions are not separated. This is a revision comparison, not an authorship-classification benchmark.'},'variants':{'baseline':display}}
 samples.append(s);print(s['id'],group,n)
(OUT/'samples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2)+'\n')
