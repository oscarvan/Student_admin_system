-- MySQL dump 10.13  Distrib 5.7.24, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: computingForFree
-- ------------------------------------------------------
-- Server version	5.7.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attenbooking`
--

DROP TABLE IF EXISTS `attenbooking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attenbooking` (
  `attenbookingID` int(11) NOT NULL AUTO_INCREMENT,
  `studentID` int(11) NOT NULL,
  `sessionID` int(11) NOT NULL,
  `actionTime` date NOT NULL,
  `action` varchar(45) NOT NULL,
  `lastEngagement` date DEFAULT NULL,
  `note` varchar(4000) DEFAULT NULL,
  PRIMARY KEY (`attenbookingID`),
  KEY `studentID_idx` (`studentID`),
  KEY `sessionIDAB` (`sessionID`),
  CONSTRAINT `sessionIDAB` FOREIGN KEY (`sessionID`) REFERENCES `cSession` (`sessionID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `studentIDAB` FOREIGN KEY (`studentID`) REFERENCES `student` (`studentID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attenbooking`
--

LOCK TABLES `attenbooking` WRITE;
/*!40000 ALTER TABLE `attenbooking` DISABLE KEYS */;
INSERT INTO `attenbooking` VALUES (1,1111113,4,'2018-11-01','book',NULL,NULL),(2,1111111,5,'2018-11-02','book',NULL,NULL),(3,1111110,6,'2018-11-03','book',NULL,NULL),(4,1111115,1,'2018-11-05','book',NULL,NULL),(5,1111114,2,'2018-11-06','book',NULL,NULL),(6,1111112,3,'2018-11-07','book',NULL,NULL);
/*!40000 ALTER TABLE `attenbooking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cSession`
--

DROP TABLE IF EXISTS `cSession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cSession` (
  `sessionID` int(11) NOT NULL AUTO_INCREMENT,
  `campusID` int(11) NOT NULL,
  `SessionPeriod` varchar(45) NOT NULL,
  `SessionDay` varchar(45) NOT NULL,
  PRIMARY KEY (`sessionID`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `campusIDS` FOREIGN KEY (`campusID`) REFERENCES `campus` (`campusID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cSession`
--

LOCK TABLES `cSession` WRITE;
/*!40000 ALTER TABLE `cSession` DISABLE KEYS */;
INSERT INTO `cSession` VALUES (1,1,'A','MO'),(2,1,'A','TU'),(3,1,'A','WE'),(4,1,'A','TH'),(5,1,'A','FR'),(6,1,'A','SA'),(7,1,'P','MO'),(8,1,'P','TU'),(9,1,'P','WE'),(10,1,'P','TH'),(11,1,'P','FR'),(12,1,'P','SA'),(13,1,'E','MO'),(14,1,'E','TU'),(15,1,'E','WE'),(16,1,'E','TH'),(17,1,'E','FR'),(18,1,'E','SA'),(19,2,'A','MO'),(20,2,'A','TU'),(21,2,'A','WE'),(22,2,'A','TH'),(23,2,'A','FR'),(24,2,'A','SA'),(25,2,'P','MO'),(26,2,'P','TU'),(27,2,'P','WE'),(28,2,'P','TH'),(29,2,'P','FR'),(30,2,'P','SA'),(31,2,'E','MO'),(32,2,'E','TU'),(33,2,'E','WE'),(34,2,'E','TH'),(35,2,'E','FR'),(36,2,'E','SA'),(37,3,'A','MO'),(38,3,'A','TU'),(39,3,'A','WE'),(40,3,'A','TH'),(41,3,'A','FR'),(42,3,'A','SA'),(43,3,'P','MO'),(44,3,'P','TU'),(45,3,'P','WE'),(46,3,'P','TH'),(47,3,'P','FR'),(48,3,'P','SA'),(49,3,'E','MO'),(50,3,'E','TU'),(51,3,'E','WE'),(52,3,'E','TH'),(53,3,'E','FR'),(54,3,'E','SA'),(55,4,'A','MO'),(56,4,'A','TU'),(57,4,'A','WE'),(58,4,'A','TH'),(59,4,'A','FR'),(60,4,'A','SA'),(61,4,'P','MO'),(62,4,'P','TU'),(63,4,'P','WE'),(64,4,'P','TH'),(65,4,'P','FR'),(66,4,'P','SA'),(67,4,'E','MO'),(68,4,'E','TU'),(69,4,'E','WE'),(70,4,'E','TH'),(71,4,'E','FR'),(72,4,'E','SA'),(73,5,'A','MO'),(74,5,'A','TU'),(75,5,'A','WE'),(76,5,'A','TH'),(77,5,'A','FR'),(78,5,'A','SA'),(79,5,'P','MO'),(80,5,'P','TU'),(81,5,'P','WE'),(82,5,'P','TH'),(83,5,'P','FR'),(84,5,'P','SA'),(85,5,'E','MO'),(86,5,'E','TU'),(87,5,'E','WE'),(88,5,'E','TH'),(89,5,'E','FR'),(90,5,'E','SA'),(91,6,'A','MO'),(92,6,'A','TU'),(93,6,'A','WE'),(94,6,'A','TH'),(95,6,'A','FR'),(96,6,'A','SA'),(97,6,'P','MO'),(98,6,'P','TU'),(99,6,'P','WE'),(100,6,'P','TH'),(101,6,'P','FR'),(102,6,'P','SA'),(103,6,'E','MO'),(104,6,'E','TU'),(105,6,'E','WE'),(106,6,'E','TH'),(107,6,'E','FR'),(108,6,'E','SA'),(109,7,'A','MO'),(110,7,'A','TU'),(111,7,'A','WE'),(112,7,'A','TH'),(113,7,'A','FR'),(114,7,'A','SA'),(115,7,'P','MO'),(116,7,'P','TU'),(117,7,'P','WE'),(118,7,'P','TH'),(119,7,'P','FR'),(120,7,'P','SA'),(121,7,'E','MO'),(122,7,'E','TU'),(123,7,'E','WE'),(124,7,'E','TH'),(125,7,'E','FR'),(126,7,'E','SA');
/*!40000 ALTER TABLE `cSession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus`
--

DROP TABLE IF EXISTS `campus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campus` (
  `campusID` int(11) NOT NULL AUTO_INCREMENT,
  `campusName` varchar(200) DEFAULT NULL,
  `capacity` int(11) NOT NULL DEFAULT '20',
  PRIMARY KEY (`campusID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus`
--

LOCK TABLES `campus` WRITE;
/*!40000 ALTER TABLE `campus` DISABLE KEYS */;
INSERT INTO `campus` VALUES (1,'Ara City',20),(2,'Bishopdale',20),(3,'Hornby',20),(4,'New Brighton ',20),(5,'Rangiora ',20),(6,'Timaru',20),(7,'Oamaru',20);
/*!40000 ALTER TABLE `campus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseinfo`
--

DROP TABLE IF EXISTS `courseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseinfo` (
  `courseID` varchar(45) NOT NULL,
  `courseName` varchar(200) NOT NULL,
  `program` varchar(45) NOT NULL,
  `durationInDay` int(11) NOT NULL,
  `durationInWeek` int(11) NOT NULL,
  `numberOfSession` int(11) NOT NULL,
  `courseAvailability` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`courseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseinfo`
--

LOCK TABLES `courseinfo` WRITE;
/*!40000 ALTER TABLE `courseinfo` DISABLE KEYS */;
INSERT INTO `courseinfo` VALUES ('CFCB110','Computing Basics','ACE',70,10,20,1),('CFDB110','Access for Beginners','ACE',56,8,16,1),('CFDB310','Access Enhanced','ACE',63,9,18,1),('CFDC110','Digital Communications for Beginners','ACE',35,5,10,1),('CFDK110','Publisher for Beginners','ACE',70,10,20,1),('CFKY110','Keyboarding for Beginners','ACE',42,6,12,1),('CFPP110','PowerPoint for Beginners','ACE',35,5,10,1),('CFPS110','Photoshop for Beginners','ACE',70,10,20,1),('CFSP110','Excel for Beginners','ACE',70,10,20,1),('CFSP310','Excel Enhanced','ACE',56,8,16,1),('CFWB110','Web Design for Beginners','ACE',70,10,20,1),('CFWP110','Word for Beginners','ACE',70,10,20,1),('CFWP310','Word Enhanced','ACE',84,12,24,1),('ITTL300','Operating in a Digital Environment','Level 3',112,16,32,1),('ITTL310','Spreadsheets and Databases','Level 3',112,16,32,1),('ITTL320','Web Fundamentals','Level 3',112,16,32,1),('ITTL330','Presenting in a Digital Environment','Level 3',112,16,32,1),('ITTL340','Going Mobile','Level 3',112,16,32,1),('ITTL350','Online Etiquette and Ethics','Level 3',112,16,32,1),('ITTL400','Advanced Tools A','Level 4',112,16,32,1),('ITTL410','Advanced Tools B','Level 4',112,16,32,1),('ITTL420','Project Planning','Level 4',112,16,32,1),('ITTL430','Problem Solving','Level 4',112,16,32,1),('ITTL440','Connecting in a Business Environment','Level 4',112,16,32,1),('ITTL450','Security and Future Trends','Level 4',112,16,32,1);
/*!40000 ALTER TABLE `courseinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolment`
--

DROP TABLE IF EXISTS `enrolment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrolment` (
  `enrolmentID` int(11) NOT NULL AUTO_INCREMENT,
  `courseID` varchar(45) NOT NULL,
  `campusID` int(11) NOT NULL,
  `studentID` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date DEFAULT NULL,
  `lastWithdrawDate` date DEFAULT NULL,
  `actualWithdrawDate` date DEFAULT NULL,
  `actualEndDate` date DEFAULT NULL,
  `completed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`enrolmentID`),
  KEY `studentID_idx` (`studentID`),
  KEY `courseID_idx` (`courseID`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `studentID` FOREIGN KEY (`studentID`) REFERENCES `student` (`studentID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolment`
--

LOCK TABLES `enrolment` WRITE;
/*!40000 ALTER TABLE `enrolment` DISABLE KEYS */;
INSERT INTO `enrolment` VALUES (1,'CFCB110',1,1111112,'2018-10-10','2018-12-11','2018-10-17',NULL,NULL,0),(2,'CFCB110',1,1111111,'2018-10-10','2018-12-11','2018-10-17',NULL,NULL,0),(3,'CFCB110',1,1111113,'2018-10-10','2018-12-11','2018-10-17',NULL,NULL,0),(4,'CFCB110',1,1111114,'2018-10-10','2018-12-11','2018-10-17',NULL,NULL,0),(5,'CFCB110',1,1111115,'2018-10-10','2018-12-11','2018-10-17',NULL,NULL,0),(6,'CFCB110',1,1111110,'2018-10-10','2018-12-11','2018-10-17',NULL,NULL,0);
/*!40000 ALTER TABLE `enrolment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `noSession`
--

DROP TABLE IF EXISTS `noSession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `noSession` (
  `noSessionID` int(11) NOT NULL AUTO_INCREMENT,
  `campusID` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `sessionPeriod` varchar(45) NOT NULL,
  `weekday` varchar(45) NOT NULL,
  PRIMARY KEY (`noSessionID`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `campusIDNS` FOREIGN KEY (`campusID`) REFERENCES `campus` (`campusID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `noSession`
--

LOCK TABLES `noSession` WRITE;
/*!40000 ALTER TABLE `noSession` DISABLE KEYS */;
/*!40000 ALTER TABLE `noSession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `studentID` int(11) NOT NULL,
  `firstName` varchar(45) NOT NULL,
  `middleName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) NOT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `homePhoneNumber` varchar(45) DEFAULT NULL,
  `mobileNumber` varchar(45) DEFAULT NULL,
  `emailAddress` varchar(200) DEFAULT NULL,
  `note` varchar(4000) DEFAULT NULL,
  PRIMARY KEY (`studentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1111110,'Zahir','','Prince','M','','534138646','sodales.at.velit@dapibus.ca',''),(1111111,'Frances','','Slater','F','','907 538 4686','rutrum.justo.Praesent@tortornibh.co.uk',''),(1111112,'Lester','','Mayer','X','','665 451 0322','est.arcu.ac@metusIn.com',''),(1111113,'Britanney','','English','M','','513 793 0200','a@Cumsociisnatoque.co.uk',''),(1111114,'Norman','','Buchanan','F','','477 259 6716','ac.libero@maurissapiencursus.ca',''),(1111115,'Leah','','Hurst','X','','024 437 8808','netus.et@nonsollicitudina.com',''),(1111116,'Wylie','','Osborne','M','','563 320 1141','arcu.Sed.eu@Sedmalesuadaaugue.org',''),(1111117,'Amal','','Tanner','F','','761 851 4461','id@sitametrisus.org',''),(1111118,'Owen','','Lawson','X','','721 188 5083','mollis@ullamcorpervelit.co.uk',''),(1111119,'Sarah','','Blankenship','M','','343 565 6738','varius.orci@Nunc.edu',''),(1111120,'Yardley','','Stone','F','','017 270 9516','non.nisi@semNullainterdum.com',''),(1111121,'Lavinia','','Rogers','X','','372 172 0707','turpis.In.condimentum@vestibulumneceuismod.net',''),(1111122,'Ross','','Goodwin','M','','141 998 6831','urna.convallis@varius.org',''),(1111123,'Hedy','','Hartman','F','','953 357 5698','purus.in@blanditat.ca',''),(1111124,'Charlotte','','Delaney','X','','532 330 4942','ut.mi.Duis@orciadipiscingnon.net',''),(1111125,'Althea','','Hester','M','','540 012 6616','amet.dapibus@placeratorci.co.uk',''),(1111126,'Dahlia','','Webb','F','','176 282 2176','massa.Vestibulum@feugiatplacerat.com',''),(1111127,'Rana','','Livingston','X','','152 294 2639','Phasellus@vulputateeu.net',''),(1111128,'Karleigh','','Dudley','M','','458 282 9275','velit.eu@Nullaegetmetus.org',''),(1111129,'Stacey','','Hale','F','','609 623 3518','semper@tellus.org',''),(1111130,'Kitra','','Robles','X','','900 209 0042','pede.blandit@ornarelibero.net',''),(1111131,'Shannon','','Mathews','M','','449 568 5292','arcu.Curabitur.ut@nunc.org',''),(1111132,'Owen','','Pickett','F','','404 098 8013','Aliquam.auctor.velit@CurabiturdictumPhasellus.org',''),(1111133,'Jackson','','Sampson','X','','028 901 6468','Mauris.molestie.pharetra@atlacusQuisque.ca',''),(1111134,'Ella','','Wagner','M','','934 138 6173','urna.convallis.erat@ametante.ca',''),(1111135,'Ray','','Garner','F','','184 123 2350','convallis.ligula@ultriciesligulaNullam.org',''),(1111136,'Patrick','','Olsen','X','','093 220 4776','et@Sedcongue.ca',''),(1111137,'Madison','','Ramirez','M','','498 439 3411','suscipit@mollisvitae.org',''),(1111138,'Perry','','Schmidt','F','','251 892 7624','neque@orcitinciduntadipiscing.ca',''),(1111139,'Cairo','','Wood','X','','606 309 4361','eu.ultrices@dictumauguemalesuada.com',''),(1111140,'Wyoming','','Maddox','M','','226 495 4585','Proin.sed@hendrerit.net',''),(1111141,'Cassady','','Sanders','F','','041 050 8853','nibh.vulputate@metussitamet.edu',''),(1111142,'Ian','','Patton','X','','250 810 8919','sem@lorem.net',''),(1111143,'Rylee','','Sherman','M','','793 851 0697','pellentesque.Sed@vitaeposuereat.edu',''),(1111144,'Karen','','Moon','F','','492 237 1370','accumsan@AliquamnislNulla.co.uk',''),(1111145,'Lucian','','Maxwell','X','','021 795 0885','cursus.in@Suspendisse.edu',''),(1111146,'Grace','','Wynn','M','','062 027 2625','ut.eros.non@egetmetusIn.co.uk',''),(1111147,'Xandra','','Melendez','F','','016 054 1133','erat.neque.non@neque.co.uk',''),(1111148,'Arden','','Gill','X','','100 572 8375','purus.Nullam.scelerisque@enimdiamvel.edu',''),(1111149,'Phoebe','','Mccarty','M','','341 466 2284','lorem.eu@lobortis.com',''),(1111150,'Seth','','Burns','F','','177 758 5054','augue.ac.ipsum@ligula.edu',''),(1111151,'Elliott','','Thompson','X','','590 986 1840','vestibulum.nec.euismod@in.co.uk',''),(1111152,'Ayanna','','Roberson','M','','464 684 7121','quam@Utnecurna.edu',''),(1111153,'Oscar','','Ramos','F','','229 749 8774','cursus.a@ametrisusDonec.co.uk',''),(1111154,'Alexandra','','Fitzpatrick','X','','984 493 3456','egestas.a.scelerisque@nuncullamcorpereu.ca',''),(1111155,'Savannah','','Baldwin','M','','807 706 4501','vulputate.risus.a@ac.org',''),(1111156,'Rahim','','Garza','F','','000 922 2930','arcu.Curabitur.ut@Fuscealiquamenim.ca',''),(1111157,'Price','','Humphrey','X','','031 410 9760','ultrices@Aliquamornare.co.uk',''),(1111158,'Cooper','','Rose','M','','306 503 8375','arcu@pulvinar.org',''),(1111159,'Lisandra','','Acosta','F','','628 550 1371','non.luctus.sit@aliquetmetusurna.com',''),(1111160,'Moana','','Riddle','X','','872 524 3605','vitae.semper.egestas@aliquet.co.uk',''),(1111161,'Callum','','Jones','M','','432 437 8218','Sed@Etiambibendumfermentum.edu',''),(1111162,'Shad','','Cantrell','F','','629 244 3850','aliquam@Nunccommodo.com',''),(1111163,'Wynne','','Shelton','X','','107 950 2230','Phasellus@egetvolutpat.co.uk',''),(1111164,'Norman','','Whitfield','M','','965 858 4615','nascetur.ridiculus.mus@sed.com',''),(1111165,'Chancellor','','Short','F','','637 234 4845','nisi@seddolorFusce.edu',''),(1111166,'Marny','','Kemp','X','','844 755 2773','nec.ante.Maecenas@eu.ca',''),(1111167,'Scarlett','','Madden','M','','836 596 2115','magnis@musProin.com',''),(1111168,'Alfonso','','Sanders','F','','349 512 0545','Sed.nulla.ante@metusurna.co.uk',''),(1111169,'Aurelia','','Garner','X','','307 309 5764','tincidunt.orci.quis@lectus.com',''),(1111170,'Andrew','','Glass','M','','386 073 4370','sed.dui@Namporttitorscelerisque.edu',''),(1111171,'Keane','','Oconnor','F','','843 753 4502','diam@anteVivamusnon.co.uk',''),(1111172,'Allistair','','Berry','X','','758 662 7489','mauris.blandit.mattis@velitegestas.net',''),(1111173,'Denton','','Beard','M','','147 097 6424','sed.sem@ornareFuscemollis.com',''),(1111174,'Theodore','','Ashley','F','','209 295 5209','eleifend.vitae.erat@amet.ca',''),(1111175,'Rylee','','Hays','X','','844 124 6036','mollis.vitae@blanditmattisCras.ca',''),(1111176,'Vanna','','Summers','M','','967 366 2440','mollis@Aliquamauctor.edu',''),(1111177,'Nola','','Nelson','F','','785 735 2315','magnis.dis.parturient@neceleifendnon.co.uk',''),(1111178,'Orson','','Abbott','X','','351 782 5993','aliquet.metus@quis.com',''),(1111179,'Forrest','','Hayden','M','','479 217 8423','nisl@maurisidsapien.net',''),(1111180,'Deacon','','Tate','F','','770 074 2336','faucibus.leo.in@mollisnec.ca',''),(1111181,'Anjolie','','Fields','X','','609 589 4583','purus.Maecenas@elementum.edu',''),(1111182,'Deirdre','','Tyson','M','','902 847 2224','euismod@Donecelementum.org',''),(1111183,'Cyrus','','Carson','F','','602 120 5561','ut.dolor@sem.co.uk',''),(1111184,'Perry','','Day','X','','944 192 4085','et@inhendreritconsectetuer.co.uk',''),(1111185,'Brennan','','Burke','M','','609 488 7502','sit.amet.consectetuer@tristiquesenectus.com',''),(1111186,'Timothy','','Gamble','F','','192 738 3209','adipiscing@ipsum.com',''),(1111187,'Rhona','','Saunders','X','','569 830 7354','ligula.Aliquam@Aliquamnec.ca',''),(1111188,'Rinah','','Sanford','M','','665 082 8839','tristique.senectus@Quisque.edu',''),(1111189,'Derek','','Lawson','F','','205 037 1114','Fusce.dolor.quam@sitamet.co.uk',''),(1111190,'Erica','','Santana','X','','503 863 4850','ac.mattis.velit@ornarelectusante.edu',''),(1111191,'Devin','','Powell','M','','467 493 7543','quam.Pellentesque.habitant@litoratorquent.ca',''),(1111192,'Mark','','Bean','F','','520 069 9227','sit@convallisin.edu',''),(1111193,'Uriel','','Guerra','X','','486 327 2579','aliquam@Etiamlaoreet.co.uk',''),(1111194,'Fredericka','','Hyde','M','','804 327 9065','rhoncus.Donec@imperdietdictum.ca',''),(1111195,'Germane','','Gregory','F','','727 604 3637','arcu.et.pede@ametluctus.ca',''),(1111196,'Fuller','','Fitzgerald','X','','767 864 5761','sodales.purus@Sed.com',''),(1111197,'Yoshio','','Hobbs','M','','999 092 5277','lacus@facilisismagna.org',''),(1111198,'Reece','','Richards','F','','910 561 8769','amet.orci.Ut@anunc.edu',''),(1111199,'Dean','','Beasley','X','','658 655 1748','enim.Sed@Donecconsectetuer.org',''),(1111200,'Hilda','','Estes','M','','393 812 9091','Nullam.ut.nisi@Proineget.co.uk',''),(1111201,'Kelly','','Moore','F','','831 232 1378','eleifend.Cras.sed@etultricesposuere.ca',''),(1111202,'Kirsten','','Franklin','X','','423 395 4426','erat@euismodestarcu.net',''),(1111203,'Sade','','Frazier','M','','331 463 6371','Duis.mi@scelerisqueduiSuspendisse.ca',''),(1111204,'Cora','','Knight','F','','073 881 2576','vulputate.eu@uterat.co.uk',''),(1111205,'Jerome','','Gomez','X','','260 110 4651','conubia.nostra@Sedeget.net',''),(1111206,'Ivana','','Bonner','M','','418 501 8866','ut.aliquam@infaucibusorci.edu',''),(1111207,'Brent','','Fitzgerald','F','','884 809 9835','diam@Vivamuseuismod.co.uk',''),(1111208,'Carissa','','Walker','X','','534 041 5335','aliquet@aauctornon.com',''),(1111209,'Rhonda','','Vinson','M','','221 034 5935','Duis.sit@dictum.edu','');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campusID` int(11) NOT NULL,
  `firstName` varchar(45) NOT NULL,
  `middleName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `userName` varchar(45) DEFAULT NULL,
  `password_hash` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `campusIDU` FOREIGN KEY (`campusID`) REFERENCES `campus` (`campusID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,3,'Julie',NULL,'Stalker','julie@gmail.com','julie','pbkdf2:sha256:50000$vtniEKrL$372b8d641fb8af2488ad1d39ff811fa8e69bf3088b1ce8d18fe8ed676b57c12b'),(2,1,'Lois',NULL,'Li','lois@gmail.com','lois','pbkdf2:sha256:50000$vtniEKrL$372b8d641fb8af2488ad1d39ff811fa8e69bf3088b1ce8d18fe8ed676b57c12b'),(3,2,'Lois',NULL,'Sand','lois@gmail.com','lois','pbkdf2:sha256:50000$vtniEKrL$372b8d641fb8af2488ad1d39ff811fa8e69bf3088b1ce8d18fe8ed676b57c12b'),(4,5,'Kattia',NULL,'Silva','kattia@gmail.com','Kattia','pbkdf2:sha256:50000$vtniEKrL$372b8d641fb8af2488ad1d39ff811fa8e69bf3088b1ce8d18fe8ed676b57c12b'),(5,5,'Oscar',NULL,'Vanhanen','oscar@gmail.com','Oscar','pbkdf2:sha256:50000$vtniEKrL$372b8d641fb8af2488ad1d39ff811fa8e69bf3088b1ce8d18fe8ed676b57c12b');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-01  1:00:25
