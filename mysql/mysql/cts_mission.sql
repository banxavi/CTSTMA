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
-- Table structure for table `mission`
--

DROP TABLE IF EXISTS `mission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mission` (
  `id_mission` int NOT NULL AUTO_INCREMENT,
  `name_mission` varchar(45) DEFAULT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `point` int DEFAULT NULL,
  `mota` varchar(500) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `sum_mission` int DEFAULT NULL,
  PRIMARY KEY (`id_mission`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission`
--

LOCK TABLES `mission` WRITE;
/*!40000 ALTER TABLE `mission` DISABLE KEYS */;
INSERT INTO `mission` VALUES (1,'code từ sáng đến tối','2021-04-04','2022-04-04',200,'code từ ngày này qua ngày khác','con',9),(2,'Đi nhậu giải nhất','2021-04-04','2022-04-04',501,'Da banh tip cho tma','Còn',60),(3,'Câu cá auto dính','2021-04-04','2022-04-04',50,'Da banh tip cho tma','Còn',12),(4,'Ăn cơm','2022-04-01','2021-01-01',30,'Ăn cơm rô phi','Còn',44),(5,'Coder','2021-04-01','2022-01-01',40,'Ăn cơm','Còn',41),(6,'Ngu','2021-01-01','2022-01-01',22,'an com','CON',22),(8,'Cố gắng thật hạnh phúc nhé con','2021-03-05','2021-03-27',1000,'abc        \r\n                        ','Còn',600),(9,'haha','2021-03-02','2021-03-28',10020,'a\r                         ','Huy',6030),(10,'Cố gắng thật hạnh phúc nhé con','2021-03-05','2021-04-02',213,'123        \r\n                        ','Còn',123),(11,'a','2021-04-04','2021-04-04',1,'anh yeu em','Con',4),(12,'Cố gắng thật hạnh phúc nhé con','2021-03-03','2021-04-03',1000,'123','Còn',600);
/*!40000 ALTER TABLE `mission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-26  8:12:19
