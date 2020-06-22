DROP DATABASE `computingForFree`;
CREATE DATABASE `computingForFree` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `computingForFree`;

DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `studentID` int(11) NOT NULL,
  `firstName` varchar(45) NOT NULL,
  `middleName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) NOT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `homePhoneNumber` varchar(45) DEFAULT NULL,
  `mobileNumber` varchar(45) DEFAULT NULL,
  `emailAddress` varchar(200) DEFAULT NULL,
  `note` varchar(4000)DEFAULT NULL,   # This note is for admin staff to put some general notes
  PRIMARY KEY (`studentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `campus`;
CREATE TABLE IF NOT EXISTS `campus` (
  `campusID` int(11) NOT NULL AUTO_INCREMENT,
  `campusName` varchar(200) DEFAULT NULL,
  `capacity` int(11) NOT NULL DEFAULT '20',
  PRIMARY KEY (`campusID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `campusID` int(11) NOT NULL,
  `firstName` varchar(45) NOT NULL,
  `middleName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `userName` varchar(45) DEFAULT NULL,
  `password` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `campusIDU` FOREIGN KEY (`campusID`) REFERENCES `campus` (`campusID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE user CHANGE `userID` `id` INT (11) NOT NULL AUTO_INCREMENT;
ALTER TABLE user CHANGE `password` `password_hash` VARCHAR (1000);

DROP TABLE IF EXISTS `cSession`;
CREATE TABLE `cSession` (
 `sessionID` int(11) NOT NULL AUTO_INCREMENT,
 `campusID` int(11) NOT NULL,
 `SessionPeriod` varchar(45) NOT NULL,      #sessionPeriod: A,P,E
 `SessionDay` varchar(45) NOT NULL,         #sessionDay:MO,TU,WE,TH,FR,SA
 PRIMARY KEY (`sessionID`),
 KEY `campusID_idx` (`campusID`),
 CONSTRAINT `campusIDS` FOREIGN KEY (`campusID`) REFERENCES `campus` (`campusID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `noSession`;
CREATE TABLE IF NOT EXISTS `noSession` (
  `noSessionID` int(11) NOT NULL AUTO_INCREMENT,
  `campusID` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `sessionPeriod` varchar(45) NOT NULL,    # sessionPeriods are: A,P,E
  `weekday` varchar(45) NOT NULL,
  PRIMARY KEY (`noSessionID`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `campusIDNS` FOREIGN KEY (`campusID`) REFERENCES `campus` (`campusID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `courseinfo`;
CREATE TABLE IF NOT EXISTS `courseinfo` (
  `courseID` varchar(45) NOT NULL,
  `courseName` varchar(200) NOT NULL,
  `program` varchar(45) NOT NULL,
  `durationInDay` int(11) NOT NULL,
  `durationInWeek` int(11) NOT NULL,
  `numberOfSession` int(11) NOT NULL,      # the length of the whole program
  PRIMARY KEY (`courseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `computingForFree`.`courseinfo`
ADD COLUMN `courseAvailability` TINYINT NOT NULL DEFAULT 1 AFTER `numberOfSession`; # a boolean for if a course is still available, 1 for true, 0 for false


DROP TABLE IF EXISTS `enrolment`;
CREATE TABLE IF NOT EXISTS `enrolment` (
  `enrolmentID` int(11) NOT NULL AUTO_INCREMENT,
  `courseID` varchar(45) NOT NULL,
  `campusID` int(11) NOT NULL,
  `studentID` int(11) NOT NULL,
  `startDate` date NOT NULL,       #the day a student start the course
  `endDate` date DEFAULT NULL,     # the day a student supposed to finish the course, cannot exceed 11DEC in a year
  `lastWithdrawDate` date DEFAULT NULL,   # the day pass 10% of the study
  `actualWithdrawDate` date DEFAULT NULL,  # the day a student withdraw from the course
  `actualEndDate` date DEFAULT NULL,      #  the day a student actually finish the course
  PRIMARY KEY (`enrolmentID`),
  KEY `studentID_idx` (`studentID`),
  KEY `courseID_idx` (`courseID`),
  KEY `campusID_idx` (`campusID`),
  CONSTRAINT `studentID` FOREIGN KEY (`studentID`) REFERENCES `student` (`studentID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `computingForFree`.`enrolment`
ADD COLUMN `completed` TINYINT NOT NULL DEFAULT 0 AFTER `actualEndDate`;   # a boolean of a student's study completed or not 1 means true, 0 means false

INSERT INTO `enrolment` (`courseID`, `campusID`, `studentID`, `startDate`, `endDate`, `lastWithdrawDate`, `actualWithdrawDate`, `actualEndDate`, `completed`) VALUES
('CFCB110', 1, 1111112, '2018-10-10', '2018-12-12', '2018-12-12', NULL, '2018-12-12', 2),
('CFCB110', 1, 1111111, '2018-10-10', '2018-12-12', '2018-12-12', NULL, '2018-12-12', 2),
('CFCB110', 1, 1111113, '2018-10-10', '2018-12-12', '2018-12-12', NULL, '2018-12-12', 2),
('CFCB110', 1, 1111114, '2018-10-10', '2018-12-12', '2018-12-12', NULL, '2018-12-12', 2),
('CFCB110', 1, 1111115, '2018-10-10', '2018-12-12', '2018-12-12', NULL, '2018-12-12', 2),
('CFCB110', 1, 1111110, '2018-10-10', '2018-12-12', '2018-12-12', NULL, '2018-12-12', 2);

DROP TABLE IF EXISTS `attenbooking`;
CREATE TABLE IF NOT EXISTS `attenbooking` (
  `attenbookingID` int(11) NOT NULL AUTO_INCREMENT,
  `studentID` int(11) NOT NULL,
  `campusID` int(11) NOT NULL,   # this feild is gone
  `actionTime` date NOT NULL,     # the date student plan to book in/ student showup/student cancel the booking/student booked but noshow
  `action` varchar(45) NOT NULL,      # actions are: book, cancel, checkin and noshow
  `sessionPeriod` varchar(45) NOT NULL,    # this field is gone 
  `lastEngagement` date NOT NULL,
  `note` varchar(4000) DEFAULT NULL,    # This note is for admin staff to put some notes related to student acction
  PRIMARY KEY (`attenbookingID`),
  KEY `studentID_idx` (`studentID`),
  CONSTRAINT `studentIDAB` FOREIGN KEY (`studentID`) REFERENCES `computingForFree`.`student` (`studentID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `attenbooking` DROP `campusID`;
ALTER TABLE `attenbooking` DROP `sessionPeriod`;
ALTER TABLE `attenbooking`
ADD COLUMN `sessionID` int(11) NOT NULL AFTER `studentID`;
ALTER TABLE `attenbooking`
ADD CONSTRAINT `sessionIDAB` FOREIGN KEY
    (`sessionID`)
    REFERENCES  `cSession`(`sessionID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
ALTER TABLE `attenbooking`
CHANGE COLUMN `lastEngagement` `lastEngagement` DATE NULL ;
