CREATE DATABASE  IF NOT EXISTS `vending`
USE `vending`;

DROP TABLE IF EXISTS `Location`;
CREATE TABLE `Location` (
  `location_id` smallint unsigned NOT NULL,
  `address` varchar(255) NOT NULL,
  `address_2` varchar(50) DEFAULT NULL,
  `zip` varchar(15) NOT NULL,
  `state` char(2) NOT NULL,
  PRIMARY KEY (`location_id`),
  UNIQUE KEY `location_id_UNIQUE` (`location_id`)
);

DROP TABLE IF EXISTS `Snack`;
CREATE TABLE `Snack` (
  `snack_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`snack_id`),
  UNIQUE KEY `snack_id_UNIQUE` (`snack_id`)
);

DROP TABLE IF EXISTS `VendingMachine`;
CREATE TABLE `VendingMachine` (
  `machine_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `location_id` smallint unsigned DEFAULT NULL,
  PRIMARY KEY (`machine_id`),
  UNIQUE KEY `machine_id_UNIQUE` (`machine_id`),
  KEY `location_id_idx` (`location_id`),
  CONSTRAINT `location_id` FOREIGN KEY (`location_id`) REFERENCES `Location` (`location_id`) ON DELETE RESTRICT ON UPDATE CASCADE
);

DROP TABLE IF EXISTS `VendingMachineSnack`;
CREATE TABLE `VendingMachineSnack` (
  `snack_id` smallint unsigned NOT NULL,
  `machine_id` smallint unsigned NOT NULL,
  `slot_code` varchar(3) NOT NULL,
  `quantity` tinyint unsigned DEFAULT '0',
  `price` decimal(10,2) unsigned DEFAULT '0.00',
  PRIMARY KEY (`machine_id`,`slot_code`),
  UNIQUE KEY `machine_id_UNIQUE` (`machine_id`),
  KEY `snack_id_idx` (`snack_id`),
  CONSTRAINT `machine_id` FOREIGN KEY (`machine_id`) REFERENCES `VendingMachine` (`machine_id`),
  CONSTRAINT `vending_machine_snack` FOREIGN KEY (`snack_id`) REFERENCES `Snack` (`snack_id`)
);

DROP TABLE IF EXISTS `Nutrition`;
CREATE TABLE `Nutrition` (
  `snack_id` smallint unsigned NOT NULL,
  `serving_size` varchar(45) NOT NULL,
  `serving_per` smallint NOT NULL,
  `calories` smallint NOT NULL,
  `total_fat` smallint NOT NULL,
  `saturated_fat` smallint DEFAULT NULL,
  `trans_fat` smallint DEFAULT NULL,
  `cholesterol` smallint NOT NULL,
  `sodium` smallint NOT NULL,
  `total_carbohydrate` smallint NOT NULL,
  `fiber` smallint DEFAULT NULL,
  `total_sugars` smallint DEFAULT NULL,
  `added_sugars` smallint DEFAULT NULL,
  `protein` smallint NOT NULL,
  `additional_info` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`snack_id`),
  UNIQUE KEY `snack_id_UNIQUE` (`snack_id`),
  CONSTRAINT `snack_nutrition` FOREIGN KEY (`snack_id`) REFERENCES `Snack` (`snack_id`) ON DELETE CASCADE ON UPDATE CASCADE
);