import {json,error,participant,view,start,sameOrigin,body} from '@/lib/server';
export async function GET(req:Request){try{const p=await participant(req,false);return json(p?await view(p):{session:null});}catch(e){return error(e);}}
export async function POST(req:Request){try{sameOrigin(req);const b=await body(req);if(b.consent!==true)return json({error:'Confirm participation to start.'},400);return await start(req);}catch(e){return error(e);}}
