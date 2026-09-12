--
-- Table structure for table `company_roles_table`
--

DROP TABLE IF EXISTS `company_roles_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_roles_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `rol` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_roles_table`
--

LOCK TABLES `company_roles_table` WRITE;
/*!40000 ALTER TABLE `company_roles_table` DISABLE KEYS */;
INSERT INTO `company_roles_table` VALUES
(1,'ADMIN','Admin'),
(2,'ENGINEER','Ingeniero'),
(3,'MANAGER','Gerente'),
(4,'SUPERVISOR','Supervisor'),
(5,'ACCOUNTING','Finanzas'),
(6,'DEPARTAMENTAL_REP','Representante departamental');
/*!40000 ALTER TABLE `company_roles_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credentials_table`
--

DROP TABLE IF EXISTS `credentials_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `mail` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `credentials_table_unique` (`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `credentials_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials_table`
--

LOCK TABLES `credentials_table` WRITE;
/*!40000 ALTER TABLE `credentials_table` DISABLE KEYS */;
INSERT INTO `credentials_table` VALUES
(1,1,'admin@gmail.com','$2b$12$3EeC7T0O8gyAmxGJeQQZpOJkhu5kie4XkYlEJaLcGw6ccRJlHNxau',1),
/*!40000 ALTER TABLE `credentials_table` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `file_tipes_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_tipes_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(100) DEFAULT NULL,
  `is_main_image` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `mime_type_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `file_tipes_table_mime_type_extension_table_FK` (`mime_type_id`),
  CONSTRAINT `file_tipes_table_mime_tipes_FK` FOREIGN KEY (`mime_type_id`) REFERENCES `mime_tipes` (`id`),
  CONSTRAINT `file_tipes_table_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_tipes_table`
--

LOCK TABLES `file_tipes_table` WRITE;
/*!40000 ALTER TABLE `file_tipes_table` DISABLE KEYS */;
INSERT INTO `file_tipes_table` VALUES
(1,'Hojas de cálculo',0,1,1),
(2,'Archivos PDF',0,1,2),
(3,'Archivo de texto',0,1,3),
(4,'Presentaciones',0,1,4),
(5,'Documento',0,1,5),
(6,'Archivo de imagen',0,1,6),
(7,'Archivo de imagen',0,1,7),
(8,'Archivo de imagen',1,1,6),
(9,'Archivo de imagen',1,1,7);
/*!40000 ALTER TABLE `file_tipes_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mime_category`
--

DROP TABLE IF EXISTS `mime_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mime_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mime_category_unique` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mime_category`
--

LOCK TABLES `mime_category` WRITE;
/*!40000 ALTER TABLE `mime_category` DISABLE KEYS */;
INSERT INTO `mime_category` VALUES
(3,'document'),
(6,'file'),
(2,'image'),
(1,'main_image'),
(5,'presentation'),
(4,'sheet');
/*!40000 ALTER TABLE `mime_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mime_tipes`
--

DROP TABLE IF EXISTS `mime_tipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mime_tipes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mime_pattern` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `category_id` int NOT NULL,
  `extension` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mime_tipes_mime_category_FK` (`category_id`),
  CONSTRAINT `mime_tipes_mime_category_FK` FOREIGN KEY (`category_id`) REFERENCES `mime_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mime_tipes`
--

LOCK TABLES `mime_tipes` WRITE;
/*!40000 ALTER TABLE `mime_tipes` DISABLE KEYS */;
INSERT INTO `mime_tipes` VALUES
(1,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','/icons/excel.svg',4,'xlsx'),
(2,'application/pdf','/icons/file.svg',6,'pdf'),
(3,'text/plain','/icons/file.svg',6,'txt'),
(4,'application/vnd.openxmlformats-officedocument.presentationml.presentation','/icons/file.svg',5,'pptx'),
(5,'application/vnd.openxmlformats-officedocument.wordprocessingml.document','/icons/word.svg',3,'docx'),
(6,'image/png','/icons/file.svg',2,'jpg'),
(7,'image/jpeg','/icons/file.svg',2,'png');
/*!40000 ALTER TABLE `mime_tipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions_table`
--

DROP TABLE IF EXISTS `permissions_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `permission` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permissions_table_unique` (`permission`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_events`
--

DROP TABLE IF EXISTS `project_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `action_id` int NOT NULL,
  `project_id` int NOT NULL,
  `approved` tinyint(1) DEFAULT '0',
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `project_events_users_table_FK` (`user_id`),
  KEY `project_events_project_table_FK` (`project_id`),
  KEY `project_events_project_status_FK` (`action_id`),
  CONSTRAINT `project_events_project_status_FK` FOREIGN KEY (`action_id`) REFERENCES `project_status` (`id`),
  CONSTRAINT `project_events_project_table_FK` FOREIGN KEY (`project_id`) REFERENCES `project_table` (`id`),
  CONSTRAINT `project_events_users_table_FK` FOREIGN KEY (`user_id`) REFERENCES `users_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_files_table`
--

DROP TABLE IF EXISTS `project_files_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_files_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `filename` varchar(50) NOT NULL,
  `path` varchar(50) NOT NULL,
  `code` varchar(70) NOT NULL,
  `file_type_id` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `file_type_id` (`file_type_id`),
  CONSTRAINT `project_files_table_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project_table` (`id`),
  CONSTRAINT `project_files_table_ibfk_2` FOREIGN KEY (`file_type_id`) REFERENCES `file_tipes_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `project_roles_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_roles_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(30) NOT NULL,
  `description` varchar(40) NOT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_roles_table_unique` (`code`),
  UNIQUE KEY `project_roles_table_unique_1` (`description`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_roles_table`
--

LOCK TABLES `project_roles_table` WRITE;
/*!40000 ALTER TABLE `project_roles_table` DISABLE KEYS */;
INSERT INTO `project_roles_table` VALUES
(1,'ADMIN','Administrador de proyecto',1),
(2,'COADMIN','Administrador colaborador',1),
(3,'COLLABORATOR','Colaborador',1),
(4,'AUDITOR','Auditor',1);
/*!40000 ALTER TABLE `project_roles_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_tipes_table`
--

DROP TABLE IF EXISTS `project_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_status` (
  `int` int NOT NULL AUTO_INCREMENT,
  `status` varchar(30) DEFAULT NULL,
  `description` varchar(40) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`int`),
  UNIQUE KEY `project_status_unique` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_status`
--

LOCK TABLES `project_status` WRITE;
/*!40000 ALTER TABLE `project_status` DISABLE KEYS */;
INSERT INTO `project_status` VALUES
(1,'PROPOSAL','Propuesta',1),
(2,'EVALUATION','Evaluación',1),
(3,'PRIORIZATION','Priorización',1),
(4,'APPROVED','Aprovación',1),
(5,'ON_PROGRESS','En progureso',1),
(6,'FINISHED','Terminado',1),
(7,'ON_HOLD','En espera',1),
(8,'CANCELED','Cancelado',1),
(9,'REFUSED','Rechazado',1);
/*!40000 ALTER TABLE `project_status` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `project_table`
--

DROP TABLE IF EXISTS `project_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text,
  `main_directory` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `priority` int DEFAULT '10',
  `status_id` int NOT NULL DEFAULT '1',
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
  KEY `project_table_project_status_FK` (`status_id`),
  CONSTRAINT `project_table_project_status_FK` FOREIGN KEY (`status_id`) REFERENCES `project_status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_users_table`
--

DROP TABLE IF EXISTS `project_users_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_users_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `project_role_id` int DEFAULT NULL,
  `project_id` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `proposal_id` (`project_id`),
  KEY `project_users_table_project_roles_table_FK` (`project_role_id`),
  CONSTRAINT `project_users_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_table` (`id`),
  CONSTRAINT `project_users_table_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project_table` (`id`),
  CONSTRAINT `project_users_table_project_roles_table_FK` FOREIGN KEY (`project_role_id`) REFERENCES `project_roles_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role_permission_table`
--

DROP TABLE IF EXISTS `role_permission_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
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
-- Table structure for table `users_table`
--

DROP TABLE IF EXISTS `users_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `first_lastname` varchar(40) NOT NULL,
  `second_lastname` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rol_id` int NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `users_table_company_roles_table_FK` FOREIGN KEY (`rol_id`) REFERENCES `company_roles_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;