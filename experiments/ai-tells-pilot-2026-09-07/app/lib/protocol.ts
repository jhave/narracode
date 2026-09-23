export const ARMS = ['baseline','september4','september5','contextual'] as const;
export type Arm = typeof ARMS[number];
export type Assignment = {sampleId:string; a:Arm; b:Arm};
export const PAIRS: [Arm,Arm][] = ARMS.flatMap((a,i)=>ARMS.slice(i+1).map(b=>[a,b] as [Arm,Arm]));
export type Rating = {voice:number|null; effect:number|null};
export type ResponseData = {preference:'A'|'B'|'tie'|'neither'|'unsure'|'skip'; ratings:{A:Rating; B:Rating}; notes:string; familiar:'yes'|'no'|'unsure'|null; seconds:number};
export function shuffle<T>(items:readonly T[], random:()=>number=Math.random):T[] { const a=[...items];for(let i=a.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a; }
export function assign(ids:string[],random:()=>number=Math.random):Assignment[] {
 if(ids.length!==12||new Set(ids).size!==12)throw new Error('The pilot requires 12 unique passages.');
 const pairs=shuffle([...PAIRS,...PAIRS],random);
 return shuffle(ids,random).map((sampleId,i)=>{const [a,b]=random()<.5?pairs[i]:[pairs[i][1],pairs[i][0]];return {sampleId,a,b};});
}
export function validateResponse(input:unknown):ResponseData {
 if(!input||typeof input!=='object') throw new Error('A response is required.');
 const x=input as Record<string,unknown>;
 if(!['A','B','tie','neither','unsure','skip'].includes(x.preference as string))throw new Error('Choose a preference, a tie, neither, unsure, or skip.');
 if(typeof x.notes!=='string'||x.notes.length>3000)throw new Error('Notes must be 3,000 characters or fewer.');
 if(![null,'yes','no','unsure'].includes(x.familiar as null|string))throw new Error('Invalid familiarity response.');
 if(typeof x.seconds!=='number'||!Number.isFinite(x.seconds)||x.seconds<0||x.seconds>86400)throw new Error('Invalid reading duration.');
 const scores=x.ratings as Record<string,Record<string,unknown>>;
 const rating=(label:string):Rating=>{
  const s=scores?.[label];if(!s||typeof s!=='object')throw new Error('Missing ratings.');
  for(const k of ['voice','effect'])if(s[k]!==null&&(!Number.isInteger(s[k])||Number(s[k])<1||Number(s[k])>5))throw new Error('Ratings must be 1–5 or unscored.');
  return {voice:s.voice as number|null,effect:s.effect as number|null};
 };
 return {preference:x.preference as ResponseData['preference'],notes:x.notes,familiar:x.familiar as ResponseData['familiar'],seconds:x.seconds,ratings:{A:rating('A'),B:rating('B')}};
}
