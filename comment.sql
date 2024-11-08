CREATE TABLE IF NOT EXISTS `users` (
	`id` int NOT NULL,
	`user_type_id` int NOT NULL,
	`email` varchar(255) NOT NULL,
	`password` varchar(255) NOT NULL,
	`username` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `comment` (
	`text` varchar(255) NOT NULL,
	`created_at` datetime NOT NULL,
	`parent` int NOT NULL,
	`home_page` varchar(255) NOT NULL,
	`id` int NOT NULL,
	`user_id` int NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `users` ADD CONSTRAINT `users_fk1` FOREIGN KEY (`user_type_id`) REFERENCES `user_types`(`id`);
ALTER TABLE `comment` ADD CONSTRAINT `comment_fk2` FOREIGN KEY (`parent`) REFERENCES `comment`(`id`);

ALTER TABLE `comment` ADD CONSTRAINT `comment_fk5` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`);