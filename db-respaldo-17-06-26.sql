-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: dbCompiladorDePropuestas
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `dbCompiladorDePropuestas`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dbCompiladorDePropuestas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `dbCompiladorDePropuestas`;

--
-- Table structure for table `credentials_table`
--

DROP TABLE IF EXISTS `credentials_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `mail` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `credentials_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials_table`
--

LOCK TABLES `credentials_table` WRITE;
/*!40000 ALTER TABLE `credentials_table` DISABLE KEYS */;
INSERT INTO `credentials_table` VALUES (1,5,'donovanhdz167@gmail.com','$2b$12$3EeC7T0O8gyAmxGJeQQZpOJkhu5kie4XkYlEJaLcGw6ccRJlHNxau',1);
/*!40000 ALTER TABLE `credentials_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `extension_file`
--

DROP TABLE IF EXISTS `extension_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `extension_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `extension` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `extension_file_unique` (`extension`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `extension_file`
--

LOCK TABLES `extension_file` WRITE;
/*!40000 ALTER TABLE `extension_file` DISABLE KEYS */;
INSERT INTO `extension_file` VALUES (5,'docx'),(7,'jpg'),(2,'pdf'),(6,'png'),(4,'pptx'),(3,'txt'),(1,'xlsx');
/*!40000 ALTER TABLE `extension_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_tipes_table`
--

DROP TABLE IF EXISTS `file_tipes_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_tipes_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(100) DEFAULT NULL,
  `is_main_image` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `mime_type_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `file_tipes_table_mime_type_extension_table_FK` (`mime_type_id`),
  CONSTRAINT `file_tipes_table_mime_type_extension_table_FK` FOREIGN KEY (`mime_type_id`) REFERENCES `mime_type_extension_table` (`id`),
  CONSTRAINT `file_tipes_table_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_tipes_table`
--

LOCK TABLES `file_tipes_table` WRITE;
/*!40000 ALTER TABLE `file_tipes_table` DISABLE KEYS */;
INSERT INTO `file_tipes_table` VALUES (1,'Hojas de cálculo',0,1,NULL),(2,'Archivos PDF',0,1,NULL),(3,'Archivo de texto',0,1,NULL),(4,'Presentaciones',0,1,NULL),(5,'Documento',0,1,NULL),(6,'Archivo de imagen',0,1,NULL),(7,'Archivo de imagen',0,1,NULL),(8,'Archivo de imagen',1,1,NULL),(9,'Archivo de imagen',1,1,NULL);
/*!40000 ALTER TABLE `file_tipes_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mime_tipes`
--

DROP TABLE IF EXISTS `mime_tipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mime_tipes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mime_pattern` varchar(30) NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `category` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mime_tipes`
--

LOCK TABLES `mime_tipes` WRITE;
/*!40000 ALTER TABLE `mime_tipes` DISABLE KEYS */;
INSERT INTO `mime_tipes` VALUES (1,'main_image',NULL,'1'),(2,'image',NULL,'1'),(3,'document',NULL,'2'),(4,'sheet',NULL,'2'),(5,'presentation',NULL,'2'),(6,'file',NULL,'2');
/*!40000 ALTER TABLE `mime_tipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mime_type_extension_table`
--

DROP TABLE IF EXISTS `mime_type_extension_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mime_type_extension_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `extension_id` int NOT NULL,
  `mime_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mime_type_extension_table_extension_file_FK` (`extension_id`),
  KEY `mime_type_extension_table_mime_tipes_FK` (`mime_type_id`),
  CONSTRAINT `mime_type_extension_table_extension_file_FK` FOREIGN KEY (`extension_id`) REFERENCES `extension_file` (`id`),
  CONSTRAINT `mime_type_extension_table_mime_tipes_FK` FOREIGN KEY (`mime_type_id`) REFERENCES `mime_tipes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mime_type_extension_table`
--

LOCK TABLES `mime_type_extension_table` WRITE;
/*!40000 ALTER TABLE `mime_type_extension_table` DISABLE KEYS */;
INSERT INTO `mime_type_extension_table` VALUES (1,1,4),(2,2,6),(3,3,6),(4,4,5),(5,5,3),(6,6,2),(7,7,2),(8,6,1),(9,7,1);
/*!40000 ALTER TABLE `mime_type_extension_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions_table`
--

DROP TABLE IF EXISTS `permissions_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `permission` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permissions_table_unique` (`permission`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions_table`
--

LOCK TABLES `permissions_table` WRITE;
/*!40000 ALTER TABLE `permissions_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `permissions_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proposal_files_table`
--

DROP TABLE IF EXISTS `proposal_files_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proposal_files_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `proposal_id` int NOT NULL,
  `filename` varchar(50) NOT NULL,
  `path` varchar(50) NOT NULL,
  `file_type_id` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proposal_id` (`proposal_id`),
  KEY `file_type_id` (`file_type_id`),
  CONSTRAINT `proposal_files_table_ibfk_1` FOREIGN KEY (`proposal_id`) REFERENCES `proposal_table` (`id`),
  CONSTRAINT `proposal_files_table_ibfk_2` FOREIGN KEY (`file_type_id`) REFERENCES `file_tipes_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proposal_files_table`
--

LOCK TABLES `proposal_files_table` WRITE;
/*!40000 ALTER TABLE `proposal_files_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `proposal_files_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proposal_table`
--

DROP TABLE IF EXISTS `proposal_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proposal_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `description` text,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proposal_table`
--

LOCK TABLES `proposal_table` WRITE;
/*!40000 ALTER TABLE `proposal_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `proposal_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proposal_users_table`
--

DROP TABLE IF EXISTS `proposal_users_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proposal_users_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `proposal_id` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `proposal_id` (`proposal_id`),
  CONSTRAINT `proposal_users_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_table` (`id`),
  CONSTRAINT `proposal_users_table_ibfk_2` FOREIGN KEY (`proposal_id`) REFERENCES `proposal_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proposal_users_table`
--

LOCK TABLES `proposal_users_table` WRITE;
/*!40000 ALTER TABLE `proposal_users_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `proposal_users_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission_table`
--

DROP TABLE IF EXISTS `role_permission_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permission_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_permission_table_roles_table_FK` (`role_id`),
  KEY `role_permission_table_permissions_table_FK` (`permission_id`),
  CONSTRAINT `role_permission_table_permissions_table_FK` FOREIGN KEY (`permission_id`) REFERENCES `permissions_table` (`id`),
  CONSTRAINT `role_permission_table_roles_table_FK` FOREIGN KEY (`role_id`) REFERENCES `roles_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission_table`
--

LOCK TABLES `role_permission_table` WRITE;
/*!40000 ALTER TABLE `role_permission_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_permission_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_table`
--

DROP TABLE IF EXISTS `roles_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_table`
--

LOCK TABLES `roles_table` WRITE;
/*!40000 ALTER TABLE `roles_table` DISABLE KEYS */;
INSERT INTO `roles_table` VALUES (1,'admin'),(2,'user');
/*!40000 ALTER TABLE `roles_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_table`
--

DROP TABLE IF EXISTS `users_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `first_lastname` varchar(40) NOT NULL,
  `second_lastname` varchar(40) NOT NULL,
  `rol_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `users_table_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_table`
--

LOCK TABLES `users_table` WRITE;
/*!40000 ALTER TABLE `users_table` DISABLE KEYS */;
INSERT INTO `users_table` VALUES (5,'Dónovan Alonso','Hernández','Carmona',2);
/*!40000 ALTER TABLE `users_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'dbCompiladorDePropuestas'
--

--
-- Dumping routines for database 'dbCompiladorDePropuestas'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-17 23:17:49
