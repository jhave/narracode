import {database} from '@/db/raw';
import {json,error,participant,view,sameOrigin,body,RequestError} from '@/lib/server';
export async function POST(req:Request){try{sameOrigin(req);await body(req);const p=(await participant(req))!;
 if(!p.closed_at){const now=new Date().toISOString();const r=await database().prepare('UPDATE participants SET closed_at=? WHERE id=? AND closed_at IS NULL AND (SELECT COUNT(*) FROM responses WHERE participant_id=?)=12').bind(now,p.id,p.id).run();if(!r.meta.changes)throw new RequestError('Review or explicitly skip each passage before finishing.',409);p.closed_at=now;}
 return json(await view(p));}catch(e){return error(e);}}
