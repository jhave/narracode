CREATE TABLE `participants` (
	`id` text PRIMARY KEY NOT NULL,
	`study_version` text NOT NULL,
	`assignments` text NOT NULL,
	`created_at` text NOT NULL,
	`closed_at` text,
	`revealed_at` text
);
--> statement-breakpoint
CREATE TABLE `responses` (
	`participant_id` text NOT NULL,
	`sample_id` text NOT NULL,
	`payload` text NOT NULL,
	`updated_at` text NOT NULL,
	PRIMARY KEY(`participant_id`, `sample_id`),
	FOREIGN KEY (`participant_id`) REFERENCES `participants`(`id`) ON UPDATE no action ON DELETE no action
);
