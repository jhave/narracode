import {database} from '@/db/raw';
import {json,error} from '@/lib/server';
export async function GET(){try{await database().prepare('SELECT COUNT(*) AS n FROM participants').first();return json({ready:true});}catch(e){return error(e);}}
