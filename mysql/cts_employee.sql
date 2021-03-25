-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: cts
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id_employee` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `password` char(100) DEFAULT NULL,
  `name_employ` varchar(45) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `deparment` varchar(45) DEFAULT NULL,
  `phonenumber` char(10) DEFAULT NULL,
  `permit` int DEFAULT NULL,
  `point` int DEFAULT NULL,
  `id_mission` int DEFAULT NULL,
  `id_gift` int DEFAULT NULL,
  `image` binary(100) DEFAULT NULL,
  PRIMARY KEY (`id_employee`),
  KEY `fk_idgift_idx` (`id_gift`),
  KEY `fk_idmission_idx` (`id_mission`),
  CONSTRAINT `fk_idgift` FOREIGN KEY (`id_gift`) REFERENCES `exchange` (`id_gitf`),
  CONSTRAINT `fk_idmission` FOREIGN KEY (`id_mission`) REFERENCES `mission` (`id_mission`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'banxavi@gmail.com','123','Nguyen Thanh Nhat','1999-10-17','Tuy An','Nam','Dev','08',1,500,1,NULL,NULL),(2,'ducngoc@gmail.com','123','Nguyen Thanh Duc','2000-10-17','Quy Nhon','Nam','Dev','04',0,400,2,NULL,NULL),(3,'banxavi@gmail.com','123','Nguyen Thanh Nhat','1999-10-17','Tuy An','Nam','Dev','08',1,500,3,NULL,NULL),(4,'ban','123','A','1999-10-14','A','Nữ','Dev','44',0,440,1,NULL,NULL);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-17 15:09:43
