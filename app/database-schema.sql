
DROP TABLE IF EXISTS `alembic_version`;


CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `book_collection`;


CREATE TABLE `book_collection` (
  `book.id` int(11) DEFAULT NULL,
  `collection.id` int(11) DEFAULT NULL,
  KEY `fk_book_collection_book.id_books` (`book.id`),
  KEY `fk_book_collection_collection.id_collections` (`collection.id`),
  CONSTRAINT `fk_book_collection_book.id_books` FOREIGN KEY (`book.id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_collection_collection.id_collections` FOREIGN KEY (`collection.id`) REFERENCES `collections` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `book_genre`;


CREATE TABLE `book_genre` (
  `book.id` int(11) DEFAULT NULL,
  `genre.id` int(11) DEFAULT NULL,
  KEY `fk_book_genre_book.id_books` (`book.id`),
  KEY `fk_book_genre_genre.id_genres` (`genre.id`),
  CONSTRAINT `fk_book_genre_book.id_books` FOREIGN KEY (`book.id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_genre_genre.id_genres` FOREIGN KEY (`genre.id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `books`;

CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `short_desc` text NOT NULL,
  `created_at` varchar(4) NOT NULL,
  `publishing_house` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `volume` int(11) NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rating_num` int(11) NOT NULL,
  `background_image_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_books_background_image_id_images` (`background_image_id`),
  CONSTRAINT `fk_books_background_image_id_images` FOREIGN KEY (`background_image_id`) REFERENCES `images` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `collections`;


CREATE TABLE `collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` text,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_collections_name` (`name`),
  KEY `fk_collections_user_id_users` (`user_id`),
  CONSTRAINT `fk_collections_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `genres`;


CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `images`;


CREATE TABLE `images` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_images_md5_hash` (`md5_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `reviews`;


CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book_id_books` (`book_id`),
  KEY `fk_reviews_user_id_users` (`user_id`),
  CONSTRAINT `fk_reviews_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_reviews_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


