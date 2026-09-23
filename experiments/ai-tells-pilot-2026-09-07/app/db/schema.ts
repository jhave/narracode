import { sqliteTable, text, integer, primaryKey } from 'drizzle-orm/sqlite-core';
export const participants = sqliteTable('participants', {
 id: text('id').primaryKey(), studyVersion: text('study_version').notNull(), assignments: text('assignments').notNull(),
 createdAt: text('created_at').notNull(), closedAt: text('closed_at'), revealedAt: text('revealed_at'),
});
export const responses = sqliteTable('responses', {
 participantId: text('participant_id').notNull().references(()=>participants.id), sampleId: text('sample_id').notNull(),
 payload: text('payload').notNull(), updatedAt: text('updated_at').notNull(),
}, (t)=>[primaryKey({columns:[t.participantId,t.sampleId]})]);
