#!/usr/bin/env python3
"""Reproduce the September 22 inventory from pinned Git objects and curated dates.
Counts projects, not versions, chapters, commits, reports, or completed-work claims.
"""
import csv,json,subprocess,sys,re
from pathlib import Path
from collections import Counter
from datetime import date,timedelta
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/2026-09-22'
AS_OF=date(2026,9,22)
BASE='490c4c9816873854ea0ba593f74e7bd352e0894d'
PINS={'origin/claude/recent-unfinished-story-CG1N8': 'd56bc17621a297672785b159821f741221b895dd', 'origin/claude/alpha-gaia-story': '9db747375cb8c2941c230077a1349dd77a6c4078', 'origin/claude/unfinished-branches-vetch-wfg9re': '1f697a82d28fe94c4cb65bbc4fb74ad04041d16f', 'origin/claude/montreal-2028-tillman-style-dazm71': '232de9587051ee9163bc852c2af469fe23691f4a', 'origin/claude/machine-liberation-story-5a9baa': '6edbaf55a2ff082096c60c979f05160b4facdaeb'}

def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()

RECOVERED=[
 ('22-05-2026_Mature_Water','Mature Water','origin/claude/recent-unfinished-story-CG1N8','Unfinished lecture project; latest story-path commit June 27. Earlier name: What Did Not Begin.'),
 ('31-07-2026_Alpha-Gaia','Alpha-Gaia','origin/claude/alpha-gaia-story','Reading page and five draft variants; dated July 31, committed August 1. Awaiting author review.'),
 ('11-08-2026_Vetch','Vetch','origin/claude/unfinished-branches-vetch-wfg9re','Eight movements plus split movement 4a, human edits, and two peripheral documents; no story index. August 11–28 writing; September 4 review.'),
 ('23-08-2026_Chauffe_Eclaire','Chauffé Éclairé','origin/claude/montreal-2028-tillman-style-dazm71','Four chapters, revised chapter four, and reading page. Attribution word count of 1,430 is stale after expansion; not used in totals.')]

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 entries=json.loads((OUT/'library-snapshot.json').read_text())['entries']
 stories=[]
 for e in entries:
  if e['kind']!='story':continue
  p='Stories written with Narracode/'+e['folder']
  commits=git('log','--reverse','--format=%H|%aI|%s',BASE,'--',p).splitlines()
  first=commits[0].split('|',2) if commits else ['','','']
  stories.append({k:e[k] for k in ['folder','title','started_date','date','declared_word_count','href']}|{'status':'indexed','first_path_commit':first[0],'first_path_commit_date':first[1],'first_path_commit_subject':first[2]})
 recovered=[]
 for folder,title,ref,note in RECOVERED:
  sha=PINS[ref];p='Stories written with Narracode/'+folder
  commits=git('log','--reverse','--format=%H|%aI|%s',sha,'--',p).splitlines()
  first=commits[0].split('|',2);last=commits[-1].split('|',2)
  d,m,y=folder[:10].split('-')
  recovered.append(dict(folder=folder,title=title,started_date=f'{y}-{m}-{d}',status='held_for_review',branch=ref,commit=sha,first_path_commit=first[0],first_path_commit_date=first[1],last_path_commit=last[0],last_path_commit_date=last[1],note=note))
 precursor_ref='origin/claude/machine-liberation-story-5a9baa'
 precursor={'title':'Machine Liberation — September 4 precursor','folder':'04-09-2026_Machine_Liberation','branch':precursor_ref,'commit':PINS[precursor_ref],'status':'alternate_attempt_excluded_from_project_total','note':'Bibliography and Chapter 1. Same central title/brief as the indexed September 8 work; not another distinct project in this census.'}
 # Count current indexed projects by original project date, not later illustrated/revised editions.
 indexed=Counter(e['started_date'] for e in stories);held=Counter(e['started_date'] for e in recovered)
 launch=date(2026,5,9);daily=[];day=launch
 while day<=AS_OF:
  key=day.isoformat();titles=[e['title'] for e in stories+recovered if e['started_date']==key]
  daily.append(dict(date=key,indexed_projects=indexed[key],held_projects=held[key],total_projects=indexed[key]+held[key],titles='; '.join(titles)))
  day+=timedelta(days=1)
 with (OUT/'daily-counts.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(daily[0]));w.writeheader();w.writerows(daily)
 monthly=[]
 for month in ['2026-05','2026-06','2026-07','2026-08','2026-09']:
  rows=[d for d in daily if d['date'].startswith(month)]
  monthly.append(dict(month=month,observed_days=len(rows),indexed_projects=sum(d['indexed_projects'] for d in rows),held_projects=sum(d['held_projects'] for d in rows),total_projects=sum(d['total_projects'] for d in rows),days_with_project_starts=sum(d['total_projects']>0 for d in rows)))
 stats=dict(as_of=AS_OF.isoformat(),launch=launch.isoformat(),elapsed_days=(AS_OF-launch).days,calendar_dates_inclusive=len(daily),indexed_works=len(stories),held_distinct_projects=len(recovered),distinct_projects=len(stories)+len(recovered),indexed_start_days=len(indexed),all_start_days=len(set(indexed)|set(held)),declared_indexed_words=sum(e['declared_word_count'] or 0 for e in stories),monthly=monthly)
 audit=dict(method='Original folder/attribution dates are project-start proxies, not verified completion dates. Public edition dates are separate. First Git timestamps are author timestamps for first visible path commits, not upload timestamps. Current reading pages include drafts. No completion rate is inferred.',base_commit=BASE,stats=stats,indexed=stories,recovered=recovered,alternate_attempts=[precursor],renames=['May10 → 10-05-2026_Exile','Slime(written-May9-2026-with-Opus4-7) → 09-05-2026_Slime','22-05-2026_What_Did_Not_Begin → 22-05-2026_Mature_Water'],daily=daily)
 (OUT/'audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
