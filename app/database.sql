
DROP TABLE IF EXISTS `alembic_version`;


CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


LOCK TABLES `alembic_version` WRITE;


INSERT INTO `alembic_version` VALUES ('7baa03583ee2');


UNLOCK TABLES;


DROP TABLE IF EXISTS `book_collection`;


CREATE TABLE `book_collection` (
  `book.id` int(11) DEFAULT NULL,
  `collection.id` int(11) DEFAULT NULL,
  KEY `fk_book_collection_book.id_books` (`book.id`),
  KEY `fk_book_collection_collection.id_collections` (`collection.id`),
  CONSTRAINT `fk_book_collection_book.id_books` FOREIGN KEY (`book.id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_collection_collection.id_collections` FOREIGN KEY (`collection.id`) REFERENCES `collections` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


LOCK TABLES `book_collection` WRITE;


INSERT INTO `book_collection` VALUES (9,3);


UNLOCK TABLES;


LOCK TABLES `users` WRITE;

INSERT INTO `users` VALUES 
(1,'user1', 'pbkdf2:sha256:260000$jdY7F8IT5ZNssYLp$90bcadc82d5751498573b4f93d109476e99b13cf58e37d4358f7741198c5f32c','Alex','Ivan', NULL,'2023-10-15 15:10:29',1),
(2,'user2', 'pbkdf2:sha256:260000$8OYIKagHRXEkEt3Z$fe42bc86b342a6a3642f35e385152246d20c0f115cf4c02c1966cd04c073b7b4','Vladimir',NULL, '2023-06-09 15:10:39',2),
(3,'user3', 'pbkdf2:sha256:260000$H5v17ssLpatJWwZP$5a8b5d1759dc40193c99c3dac9b58744084a587b9d34bc2cae15da83c3bd5d82','Medvedev','2023-10-26', '15:15:50',3),
(4,'user4', 'pbkdf2:sha256:260000$3vJXQamHzfxPWgp0$ab0b3376c5e087a8973e2d0e3d6e2d9e2fc9551d4645d80bab4a19a82fa5d02b','Alexandre', NULL,'2023-10-26', '15:18 :15',4),
(5,'user5', 'pbkdf2:sha256:260000$Y2XMfJOI0pwQxMme$2ed2cce27619585afc4a5801624ffc66c05a6c392245abaed3728deab1c8b3ff','Dupont','2023-10-26 15:19:10', 5);


UNLOCK TABLES;
