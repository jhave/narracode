import data from '@/study/samples.json';
import type {Arm,Assignment,ResponseData} from './protocol';
export const STUDY_VERSION='narracode-pilot-2026-09-07-v1';
export const armNames:Record<Arm,string>={baseline:'Archived passage · unchanged',september4:'September 4 · 29-class procedure',september5:'September 5 · 31-class procedure',contextual:'Contextual revision · experimental'};
export const samples=data as unknown as {id:string;group:string;intent:string;contentNote:string|null;source:Record<string,unknown>;variants:Record<Arm,string>}[];
export function blindSamples(assignments:Assignment[],responses:Record<string,ResponseData>){return assignments.map((a,index)=>{const s=samples.find(s=>s.id===a.sampleId);if(!s)throw new Error('Sample unavailable.');return {id:s.id,index,intent:s.intent,contentNote:s.contentNote,versions:[{label:'A',text:s.variants[a.a],words:s.variants[a.a]?.split(/\s+/).length},{label:'B',text:s.variants[a.b],words:s.variants[a.b]?.split(/\s+/).length}],response:responses[s.id]??null};});}
