import {json,error,participant,exportData} from '@/lib/server';
export async function GET(req:Request){try{const p=(await participant(req))!;return json(await exportData(p),200,{'Content-Disposition':'attachment; filename="narracode-review.json"'});}catch(e){return error(e);}}
