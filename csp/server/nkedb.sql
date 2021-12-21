-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: nkedb
-- ------------------------------------------------------
-- Server version	8.0.27-0ubuntu0.20.04.1

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
-- Table structure for table `Group`
--

DROP TABLE IF EXISTS `Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Group` (
  `Id` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `ElderId` int NOT NULL,
  `TeacherId` int NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `TeacherId_idx` (`TeacherId`),
  KEY `ElderId_idx` (`ElderId`),
  CONSTRAINT `ElderId` FOREIGN KEY (`ElderId`) REFERENCES `Users` (`UserId`),
  CONSTRAINT `TeacherId` FOREIGN KEY (`TeacherId`) REFERENCES `Users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Group`
--

LOCK TABLES `Group` WRITE;
/*!40000 ALTER TABLE `Group` DISABLE KEYS */;
/*!40000 ALTER TABLE `Group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GroupsToUsers`
--

DROP TABLE IF EXISTS `GroupsToUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GroupsToUsers` (
  `Id` int NOT NULL,
  `UserId` int NOT NULL,
  `GroupId` int NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `UserId_idx` (`UserId`),
  KEY `GroupId_idx` (`GroupId`),
  CONSTRAINT `GroupId` FOREIGN KEY (`GroupId`) REFERENCES `Group` (`Id`),
  CONSTRAINT `UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GroupsToUsers`
--

LOCK TABLES `GroupsToUsers` WRITE;
/*!40000 ALTER TABLE `GroupsToUsers` DISABLE KEYS */;
/*!40000 ALTER TABLE `GroupsToUsers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HomeWorkList`
--

DROP TABLE IF EXISTS `HomeWorkList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HomeWorkList` (
  `Id` int NOT NULL,
  `LessonId` int NOT NULL,
  `HomeWorkDesc` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_HomeWorkList_1_idx` (`LessonId`),
  CONSTRAINT `fk_HomeWorkList_1` FOREIGN KEY (`LessonId`) REFERENCES `Lessons` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HomeWorkList`
--

LOCK TABLES `HomeWorkList` WRITE;
/*!40000 ALTER TABLE `HomeWorkList` DISABLE KEYS */;
/*!40000 ALTER TABLE `HomeWorkList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Lessons`
--

DROP TABLE IF EXISTS `Lessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Lessons` (
  `Id` int NOT NULL,
  `LessonName` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lessons`
--

LOCK TABLES `Lessons` WRITE;
/*!40000 ALTER TABLE `Lessons` DISABLE KEYS */;
/*!40000 ALTER TABLE `Lessons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MarksList`
--

DROP TABLE IF EXISTS `MarksList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MarksList` (
  `Id` int NOT NULL,
  `PupilId` int NOT NULL,
  `TeacherId` int NOT NULL,
  `Mark` char(1) NOT NULL,
  `TeacherDesc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_MarksList_1_idx` (`PupilId`),
  KEY `fk_MarksList_2_idx` (`TeacherId`),
  CONSTRAINT `fk_MarksList_1` FOREIGN KEY (`PupilId`) REFERENCES `Users` (`UserId`),
  CONSTRAINT `fk_MarksList_2` FOREIGN KEY (`TeacherId`) REFERENCES `Users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MarksList`
--

LOCK TABLES `MarksList` WRITE;
/*!40000 ALTER TABLE `MarksList` DISABLE KEYS */;
/*!40000 ALTER TABLE `MarksList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MissedLessonReasons`
--

DROP TABLE IF EXISTS `MissedLessonReasons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MissedLessonReasons` (
  `Id` int NOT NULL,
  `SkipReasonName` varchar(45) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MissedLessonReasons`
--

LOCK TABLES `MissedLessonReasons` WRITE;
/*!40000 ALTER TABLE `MissedLessonReasons` DISABLE KEYS */;
/*!40000 ALTER TABLE `MissedLessonReasons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MissedLessons`
--

DROP TABLE IF EXISTS `MissedLessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MissedLessons` (
  `Id` int NOT NULL,
  `UserId` int NOT NULL,
  `SkippedLessonsDateTime` datetime NOT NULL,
  `IsSkippedAllDay` tinyint NOT NULL,
  `SkipReasonTypeId` int NOT NULL,
  `ElderDesc` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_MissedLessons_1_idx` (`UserId`),
  KEY `fk_MissedLessons_2_idx` (`SkipReasonTypeId`),
  CONSTRAINT `fk_MissedLessons_1` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`),
  CONSTRAINT `fk_MissedLessons_2` FOREIGN KEY (`SkipReasonTypeId`) REFERENCES `MissedLessonReasons` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MissedLessons`
--

LOCK TABLES `MissedLessons` WRITE;
/*!40000 ALTER TABLE `MissedLessons` DISABLE KEYS */;
/*!40000 ALTER TABLE `MissedLessons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Roles`
--

DROP TABLE IF EXISTS `Roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Roles` (
  `Id` int NOT NULL,
  `RoleName` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Roles`
--

LOCK TABLES `Roles` WRITE;
/*!40000 ALTER TABLE `Roles` DISABLE KEYS */;
INSERT INTO `Roles` VALUES (1,'Студент'),(2,'Преподаватель'),(3,'Староста группы'),(4,'Администратор');
/*!40000 ALTER TABLE `Roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ScheduleList`
--

DROP TABLE IF EXISTS `ScheduleList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ScheduleList` (
  `Id` int NOT NULL,
  `GroupId` int NOT NULL,
  `LessonId` int NOT NULL,
  `TeacherId` int NOT NULL,
  `LessonDateTime` datetime NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_ScheduleList_1_idx` (`GroupId`),
  KEY `fk_ScheduleList_2_idx` (`LessonId`),
  KEY `fk_ScheduleList_3_idx` (`TeacherId`),
  CONSTRAINT `fk_ScheduleList_1` FOREIGN KEY (`GroupId`) REFERENCES `Group` (`Id`),
  CONSTRAINT `fk_ScheduleList_2` FOREIGN KEY (`LessonId`) REFERENCES `Lessons` (`Id`),
  CONSTRAINT `fk_ScheduleList_3` FOREIGN KEY (`TeacherId`) REFERENCES `Users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ScheduleList`
--

LOCK TABLES `ScheduleList` WRITE;
/*!40000 ALTER TABLE `ScheduleList` DISABLE KEYS */;
/*!40000 ALTER TABLE `ScheduleList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `UserId` int NOT NULL AUTO_INCREMENT,
  `UserLogin` varchar(45) NOT NULL,
  `UserPassword` varchar(45) NOT NULL,
  `UserEmail` varchar(45) NOT NULL,
  `LastLoginDateTime` datetime NOT NULL,
  `UserTypeId` int NOT NULL,
  PRIMARY KEY (`UserId`),
  KEY `fk_Users_1_idx` (`UserTypeId`),
  CONSTRAINT `fk_Users_1` FOREIGN KEY (`UserTypeId`) REFERENCES `Roles` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'teststudent','teststudent','teststudent@mail.ru','2021-12-20 16:30:00',1),(2,'testteacher','testteacher','testteacher@mail.ru','2021-12-20 16:30:00',2),(3,'testelder','testelder','testelder@mail.ru','2021-12-20 16:30:00',3),(4,'testadmin','testadmin','testadm@mail.ru','2021-12-20 16:30:00',4);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-20 16:30:47
