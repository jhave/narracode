import {database} from '@/db/raw';
import {json,error,participant,sameOrigin,body,RequestError} from '@/lib/server';
import {validateResponse,type Assignment} from '@/lib/protocol';
export async function POST(req:Request){try{sameOrigin(req);const b=await body(req);const p=(await participant(req))!;if(p.closed_at)throw new RequestError('This review is finished and cannot be edited.',409);
 if(!(JSON.parse(p.assignments) as Assignment[]).some(a=>a.sampleId===b.sampleId))throw new RequestError('Passage is not in your assigned review.',400);
 let response;try{response=validateResponse(b.response);}catch(e){throw new RequestError((e as Error).message);}
 const now=new Date().toISOString();
 const result=await database().prepare('INSERT INTO responses (participant_id,sample_id,payload,updated_at) SELECT ?,?,?,? WHERE EXISTS (SELECT 1 FROM participants WHERE id=? AND closed_at IS NULL) ON CONFLICT(participant_id,sample_id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at WHERE EXISTS (SELECT 1 FROM participants WHERE id=? AND closed_at IS NULL)').bind(p.id,b.sampleId,JSON.stringify(response),now,p.id,p.id).run();
 if(!result.meta.changes)throw new RequestError('This review is already finished.',409);
 return json({saved:true,sampleId:b.sampleId,updatedAt:now});}catch(e){return error(e);}}
