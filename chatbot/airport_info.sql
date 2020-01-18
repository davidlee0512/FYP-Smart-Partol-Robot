-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: airport_info
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'restaurant'),(2,'shop'),(3,'facility');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `match`
--

DROP TABLE IF EXISTS `match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match` (
  `pid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  PRIMARY KEY (`pid`,`tid`),
  KEY `tag_idx` (`tid`),
  CONSTRAINT `place` FOREIGN KEY (`pid`) REFERENCES `place` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tag` FOREIGN KEY (`tid`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match`
--

LOCK TABLES `match` WRITE;
/*!40000 ALTER TABLE `match` DISABLE KEYS */;
INSERT INTO `match` VALUES (1,1),(2,1),(4,2),(3,6),(1,8),(3,12),(9,14),(10,15),(6,16),(6,17),(8,18),(5,20),(7,21),(7,22);
/*!40000 ALTER TABLE `match` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `place`
--

DROP TABLE IF EXISTS `place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `place` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `place`
--

LOCK TABLES `place` WRITE;
/*!40000 ALTER TABLE `place` DISABLE KEYS */;
INSERT INTO `place` VALUES (1,'McDonald\'s','shop 100, 1/F, area A, terminal 1'),(2,'KFC','shop 201, 2/F, area B, terminal 1'),(3,'Ajisen Ramen','shop 101, 1/F, area A, terminal 1'),(4,'Crystal Jade','shop 202, 2/F, area B, terminal 1'),(5,'Beauty&You','shop 120, 1/F, area D, terminal 1'),(6,'Burberry','shop 141, 1/F, area E, terminal 1'),(7,'Cartier','shop 220, 2/F, area C, terminal 1'),(8,'Chung Hwa Book Co.','shop 169, 1/F, area F, terminal 1'),(9,'toilet','t1, 1/F, area A, terminal 1'),(10,'prayer room','pr1, 2/F, area C, terminal 1');
/*!40000 ALTER TABLE `place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag` (
  `id` int(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_idx` (`cid`),
  CONSTRAINT `category` FOREIGN KEY (`cid`) REFERENCES `category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,'fast food',1),(2,'chinese food',1),(3,'thai food',1),(4,'italian food',1),(5,'french food',1),(6,'japanese food',1),(7,'hong kong food',1),(8,'hamburger',1),(9,'spaghetti',1),(10,'pizza',1),(11,'sushi',1),(12,'ramen',1),(13,'sashimi',1),(14,'toilet',3),(15,'prayer room',3),(16,'cloth',2),(17,'fashion',2),(18,'book',2),(19,'souvenir',2),(20,'cosmetic',2),(21,'jewelery',2),(22,'watch',2);
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-18 16:46:55
