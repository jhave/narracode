import {database} from '@/db/raw';
import {STUDY_VERSION, blindSamples, samples, armNames} from './study';
import {assign,type Assignment,type ResponseData} from './protocol';
export type Participant={id:string;study_version:string;assignments:string;created_at:string;closed_at:string|null;revealed_at:string|null};
const cookieName='nc_pilot_session';
export class RequestError extends Error { constructor(message:string,public status=400){super(message);} }
export function json(value:unknown,status=200,headers:Record<string,string>={}) {return Response.json(value,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff',...headers}});}
export function error(e:unknown){if(e instanceof RequestError)return json({error:e.message},e.status);console.error('Pilot request failed',e instanceof Error?e.message:'unknown');return json({error:'Could not reach study storage. Your entries are still on this page; please retry.'},503);}
export function sameOrigin(req:Request){const origin=req.headers.get('Origin');if(!origin||origin!==new URL(req.url).origin)throw new RequestError('Please submit from the reading room.',403);if(!req.headers.get('Content-Type')?.startsWith('application/json'))throw new RequestError('JSON required.',415);}
export async function body(req:Request){if(Number(req.headers.get('Content-Length')||0)>16000)throw new RequestError('Response is too large.',413);const raw=await req.text();if(raw.length>16000)throw new RequestError('Response is too large.',413);try{return JSON.parse(raw);}catch{throw new RequestError('Invalid response data.');}}
async function hash(token:string){return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(token)))).map(x=>x.toString(16).padStart(2,'0')).join('');}
export async function participant(req:Request,required=true):Promise<Participant|null>{
 const token=req.headers.get('Cookie')?.split(';').map(s=>s.trim()).find(s=>s.startsWith(cookieName+'='))?.slice(cookieName.length+1);
 if(!token||! /^[a-f0-9]{64}$/.test(token)){if(required)throw new RequestError('Start or resume your review first.',401);return null;}
 const p=await database().prepare('SELECT * FROM participants WHERE id=?').bind(await hash(token)).first<Participant>();
 if(!p){if(required)throw new RequestError('This review session could not be found.',401);return null;}
 if(p.study_version!==STUDY_VERSION)throw new RequestError('This review belongs to a previous study edition.',409);
 return p;
}
export async function start(req:Request){const existing=await participant(req,false);if(existing)return json(await view(existing));
 const token=Array.from(crypto.getRandomValues(new Uint8Array(32))).map(x=>x.toString(16).padStart(2,'0')).join('');
 const p:Participant={id:await hash(token),study_version:STUDY_VERSION,assignments:JSON.stringify(assign(samples.map(s=>s.id),()=>crypto.getRandomValues(new Uint32Array(1))[0]/4294967296)),created_at:new Date().toISOString(),closed_at:null,revealed_at:null};
 await database().prepare('INSERT INTO participants (id,study_version,assignments,created_at) VALUES (?,?,?,?)').bind(p.id,p.study_version,p.assignments,p.created_at).run();
 return json(await view(p),201,{'Set-Cookie':`${cookieName}=${token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=15552000${new URL(req.url).protocol==='https:'?'; Secure':''}`});
}
export async function saved(p:Participant){const result=await database().prepare('SELECT sample_id,payload,updated_at FROM responses WHERE participant_id=?').bind(p.id).all<{sample_id:string;payload:string;updated_at:string}>();return result.results;}
export async function view(p:Participant){const r=await saved(p);return {studyVersion:STUDY_VERSION,reviewCode:p.id.slice(0,10),closed:!!p.closed_at,revealed:!!p.revealed_at,samples:blindSamples(JSON.parse(p.assignments),Object.fromEntries(r.map(x=>[x.sample_id,JSON.parse(x.payload)])))};}
export async function exportData(p:Participant){const r=await saved(p);const assignments=JSON.parse(p.assignments) as Assignment[];return {studyVersion:STUDY_VERSION,reviewCode:p.id.slice(0,10),createdAt:p.created_at,closedAt:p.closed_at,revealedAt:p.revealed_at,responses:r.map(x=>({sampleId:x.sample_id,...JSON.parse(x.payload),updatedAt:x.updated_at})),...(p.revealed_at?{key:assignments.map(a=>({sampleId:a.sampleId,A:armNames[a.a],B:armNames[a.b]}))}:{} )};}
