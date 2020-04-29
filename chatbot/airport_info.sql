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
INSERT INTO `category` VALUES (1,'restaurant'),(2,'shop'),(3,'facility'),(4,'location');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matching`
--

DROP TABLE IF EXISTS `matching`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matching` (
  `pid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  PRIMARY KEY (`pid`,`tid`),
  KEY `tag_idx` (`tid`),
  CONSTRAINT `place` FOREIGN KEY (`pid`) REFERENCES `place` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tag` FOREIGN KEY (`tid`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matching`
--

LOCK TABLES `matching` WRITE;
/*!40000 ALTER TABLE `matching` DISABLE KEYS */;
INSERT INTO `matching` VALUES (1,1),(2,1),(4,2),(3,6),(11,6),(1,8),(11,11),(3,12),(9,14),(10,15),(6,16),(6,17),(8,18),(5,20),(7,21),(7,22),(1,23),(2,23),(3,23),(4,23),(5,23),(7,23),(8,23),(9,23),(10,23),(11,23),(6,24),(1,26),(3,26),(5,26),(6,26),(8,26),(9,26),(2,27),(4,27),(7,27),(10,27);
/*!40000 ALTER TABLE `matching` ENABLE KEYS */;
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
INSERT INTO `place` VALUES (1,'McDonald\'s','shop 100, 1/F, area A, terminal 1'),(2,'KFC','shop 201, 2/F, area B, terminal 1'),(3,'Ajisen Ramen','shop 101, 1/F, area A, terminal 1'),(4,'Crystal Jade','shop 202, 2/F, area B, terminal 1'),(5,'Beauty&You','shop 120, 1/F, area D, terminal 1'),(6,'Burberry','shop 141, 1/F, area E, terminal 2'),(7,'Cartier','shop 220, 2/F, area C, terminal 1'),(8,'Chung Hwa Book Co.','shop 169, 1/F, area F, terminal 1'),(9,'toilet','t1, 1/F, area A, terminal 1'),(10,'prayer room','pr1, 2/F, area C, terminal 1'),(11,'Fresh Sushi','somewhere, terminal 1');
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
  `contra_type` varchar(45) DEFAULT NULL,
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
INSERT INTO `tag` VALUES (1,'fast food',1,NULL),(2,'chinese food',1,NULL),(3,'thai food',1,NULL),(4,'italian food',1,NULL),(5,'french food',1,NULL),(6,'japanese food',1,NULL),(7,'hong kong food',1,NULL),(8,'hamburger',1,NULL),(9,'spaghetti',1,NULL),(10,'pizza',1,NULL),(11,'sushi',1,NULL),(12,'ramen',1,NULL),(13,'sashimi',1,NULL),(14,'toilet',3,'A'),(15,'prayer room',3,'A'),(16,'cloth',2,NULL),(17,'fashion',2,NULL),(18,'book',2,NULL),(19,'souvenir',2,NULL),(20,'cosmetic',2,NULL),(21,'jewelery',2,NULL),(22,'watch',2,NULL),(23,'terminal1',4,'B'),(24,'terminal2',4,'B'),(25,'G/F',4,'C'),(26,'1/F',4,'C'),(27,'2/F',4,'C');
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

-- Dump completed on 2020-04-29 12:20:33
