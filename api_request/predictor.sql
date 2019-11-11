-- Adminer 4.7.3 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `original_title` varchar(255) NOT NULL,
  `synopsis` text,
  `duration` int(11) NOT NULL,
  `rating` enum('TP','-12','-16','-18') NOT NULL,
  `production_budget` int(11) DEFAULT NULL,
  `marketing_budget` int(11) DEFAULT NULL,
  `release_date` date NOT NULL,
  `3d` tinyint(1) NOT NULL DEFAULT '0',
  `revenu` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `movies` (`id`, `title`, `original_title`, `synopsis`, `duration`, `rating`, `production_budget`, `marketing_budget`, `release_date`, `3d`, `revenu`) VALUES
(1,	'Joker',	'Joker',	NULL,	122,	'-12',	NULL,	NULL,	'2019-10-09',	0,	NULL),
(3,	'Star Wars, épisode VIII : Les Derniers Jedi',	'Star Wars: Episode VIII – The Last Jedi',	NULL,	152,	'-12',	NULL,	NULL,	'2017-12-13',	0,	NULL),
(4,	'Le Dindon',	'Le Dindon',	NULL,	85,	'TP',	NULL,	NULL,	'2019-09-25',	0,	NULL),
(5,	'Toy Story 4',	'Toy Story 4',	NULL,	100,	'TP',	NULL,	NULL,	'2019-06-26',	0,	NULL),
(6,	'Donne-moi des ailes',	'Donne-moi des ailes',	NULL,	113,	'TP',	NULL,	NULL,	'2019-10-09',	0,	NULL),
(12,	'Star Wars, épisode VIII : Les Derniers Jedi',	'Star Wars: Episode VIII – The Last Jedi',	NULL,	152,	'-12',	NULL,	NULL,	'2017-12-13',	0,	NULL),
(13,	'Star Wars, épisode VIII : Les Derniers Jedi',	'Star Wars: Episode VIII – The Last Jedi',	NULL,	152,	'-12',	NULL,	NULL,	'2017-12-13',	0,	NULL),
(14,	'Le Dindon',	'Le Dindon',	NULL,	85,	'TP',	NULL,	NULL,	'2019-09-25',	0,	NULL),
(15,	'Toy Story 4',	'Toy Story 4',	NULL,	100,	'TP',	NULL,	NULL,	'2019-06-26',	0,	NULL),
(16,	'Donne-moi des ailes',	'Donne-moi des ailes',	NULL,	113,	'TP',	NULL,	NULL,	'2019-10-09',	0,	NULL),
(44,	'Despicable Me',	'Despicable Me',	NULL,	95,	'TP',	NULL,	NULL,	'2010-07-09',	0,	251476985),
(47,	'Joker',	'Joker',	NULL,	122,	'TP',	NULL,	NULL,	'2019-10-04',	0,	NULL),
(49,	'Despicable Me',	'Despicable Me',	NULL,	95,	'TP',	NULL,	NULL,	'2010-07-09',	0,	251476985);

DROP TABLE IF EXISTS `people`;
CREATE TABLE `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `people` (`id`, `firstname`, `lastname`) VALUES
(1,	'Joaquin',	'Phoenix'),
(2,	'Todd',	'Phillips'),
(3,	'Scott',	'Silver'),
(12,	'Jon',	'Snow'),
(13,	'Jean',	'Dujardin'),
(14,	'Gérard',	'Depardieu'),
(15,	'Steve',	'Carell'),
(16,	'Jason',	'Segel'),
(17,	'Russell',	'Brand'),
(18,	'Julie',	'Andrews'),
(27,	'Joaquin',	'Phoenix'),
(28,	'Robert',	'De'),
(29,	'Zazie',	'Beetz'),
(30,	'Frances',	'Conroy');

-- 2019-11-08 16:05:54
