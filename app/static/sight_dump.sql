-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: sight
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `cabinet`
--

DROP TABLE IF EXISTS `cabinet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cabinet` (
  `cab_id` int(4) NOT NULL AUTO_INCREMENT,
  `room_id` int(4) NOT NULL,
  `cab_name` varchar(128) NOT NULL DEFAULT '',
  `ctime` int(4) DEFAULT NULL,
  PRIMARY KEY (`cab_id`),
  UNIQUE KEY `key_0` (`cab_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cabinet`
--

LOCK TABLES `cabinet` WRITE;
/*!40000 ALTER TABLE `cabinet` DISABLE KEYS */;
INSERT INTO `cabinet` VALUES (1,1,'E10',1458640195),(2,1,'E11',NULL),(3,1,'E12',NULL),(4,1,'E13',NULL),(5,1,'E14',NULL);
/*!40000 ALTER TABLE `cabinet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deploy`
--

DROP TABLE IF EXISTS `deploy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deploy` (
  `deploy_id` int(4) NOT NULL AUTO_INCREMENT,
  `service_id` int(4) NOT NULL,
  `deploy_name` varchar(128) NOT NULL DEFAULT '',
  `dev_id` int(4) NOT NULL,
  `is_monitor` tinyint(1) NOT NULL,
  `ctime` int(4) NOT NULL,
  `tag_1` varchar(128) DEFAULT NULL,
  `tag_2` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`deploy_id`),
  UNIQUE KEY `key_0` (`deploy_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deploy`
--

LOCK TABLES `deploy` WRITE;
/*!40000 ALTER TABLE `deploy` DISABLE KEYS */;
INSERT INTO `deploy` VALUES (1,1,'BJ-VMMARKET-01_marketing',11,1,0,'测试marketing',NULL),(2,2,'测试服务部署点',11,1,0,NULL,NULL);
/*!40000 ALTER TABLE `deploy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deploy_status`
--

DROP TABLE IF EXISTS `deploy_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deploy_status` (
  `deploy_id` int(4) NOT NULL,
  `status` smallint(6) NOT NULL COMMENT '1正常 2异常',
  `cpu` float DEFAULT NULL COMMENT 'CPU占用',
  `mem` float DEFAULT NULL COMMENT '内存',
  `diskio_read` float DEFAULT NULL COMMENT '磁盘读',
  `diskio_write` float DEFAULT NULL COMMENT '磁盘写',
  `netio_read` float DEFAULT NULL COMMENT '网络读',
  `netio_write` float DEFAULT NULL COMMENT '网络写',
  `qps` float DEFAULT NULL,
  `resptm` float DEFAULT NULL,
  `con` float DEFAULT NULL,
  `succrt` float DEFAULT NULL,
  `fd_num` int(4) DEFAULT NULL,
  `ctime` int(4) DEFAULT NULL,
  `uptime` int(4) DEFAULT NULL,
  PRIMARY KEY (`deploy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deploy_status`
--

LOCK TABLES `deploy_status` WRITE;
/*!40000 ALTER TABLE `deploy_status` DISABLE KEYS */;
INSERT INTO `deploy_status` VALUES (1,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,12345678),(2,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `deploy_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `dev_id` int(4) NOT NULL AUTO_INCREMENT,
  `dev_name` varchar(128) NOT NULL DEFAULT '',
  `type` smallint(6) NOT NULL COMMENT '1.防火墙 2.路由器 3.交换机 4.F5 5.服务器 6.虚拟机',
  `room_id` int(4) NOT NULL,
  `cab_id` int(4) NOT NULL,
  `cab_pos` varchar(32) DEFAULT NULL,
  `ip` varchar(32) DEFAULT NULL,
  `hostname` varchar(64) DEFAULT NULL,
  `cpu_type` varchar(64) DEFAULT NULL,
  `memory` int(4) DEFAULT NULL,
  `disk` varchar(32) DEFAULT NULL,
  `intro` varchar(256) DEFAULT NULL,
  `ctime` int(4) DEFAULT NULL,
  PRIMARY KEY (`dev_id`),
  UNIQUE KEY `key_0` (`dev_name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'BJ-DMZ-01',5,1,3,'40-41','192.20.10.4','BJ-DMZ-01',NULL,NULL,NULL,NULL,NULL),(2,'BJ-DMZ-02',5,1,3,'37-38','192.20.10.5','BJ-DMZ-02',NULL,NULL,NULL,NULL,NULL),(3,'BJ-DMZ-03',5,1,3,'21-22','192.20.10.6','BJ-DMZ-03',NULL,NULL,NULL,NULL,NULL),(4,'BJ-DMZ-04',5,1,3,'18-19','192.20.10.7','BJ-DMZ-04',NULL,NULL,NULL,NULL,NULL),(5,'BJ-DMZ-05',5,1,1,'29-30','192.10.10.8','BJ-DMZ-05',NULL,NULL,NULL,NULL,NULL),(6,'BJ-DMZ-06',5,1,1,'26-27','192.10.10.9','BJ-DMZ-06',NULL,NULL,NULL,NULL,NULL),(7,'BJ-DMZ-07',5,1,1,'20','192.10.10.10','BJ-DMZ-07',NULL,NULL,NULL,NULL,NULL),(8,'BJ-DMZ-08',5,1,1,'18','192.10.10.11','BJ-DMZ-08',NULL,NULL,NULL,NULL,NULL),(9,'BJ-PAY-01',5,1,2,'25-26','192.10.20.4','BJ-PAY-01',NULL,NULL,NULL,NULL,NULL),(10,'BJ-PAY-02',5,1,2,'22-23','192.10.20.5','BJ-PAY-02',NULL,NULL,NULL,NULL,NULL),(11,'BJ-VMMARKET-01',6,1,0,NULL,'192.10.2.167','BJ-VMMARKET-01',NULL,NULL,NULL,NULL,NULL),(12,'BJ-VMMARKET-02',6,1,0,NULL,'192.10.2.168','BJ-VMMARKET-02',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_rel`
--

DROP TABLE IF EXISTS `device_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_rel` (
  `dr_id` int(4) NOT NULL AUTO_INCREMENT,
  `dev_id1` int(4) NOT NULL,
  `dev_id1_port` varchar(128) NOT NULL,
  `dev_id2` int(4) NOT NULL,
  `dev_id2_port` varchar(128) NOT NULL,
  `status` smallint(6) NOT NULL COMMENT '1正常 2非正常',
  `ctime` int(4) DEFAULT NULL,
  PRIMARY KEY (`dr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_rel`
--

LOCK TABLES `device_rel` WRITE;
/*!40000 ALTER TABLE `device_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_status`
--

DROP TABLE IF EXISTS `device_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_status` (
  `dev_id` int(4) NOT NULL,
  `status` smallint(6) DEFAULT NULL,
  `cpu` float DEFAULT NULL,
  `mem` float DEFAULT NULL,
  `upload` varchar(32) DEFAULT NULL,
  `diskio_read` float DEFAULT NULL,
  `diskio_write` float DEFAULT NULL,
  `netio_read` float DEFAULT NULL,
  `netio_write` float DEFAULT NULL,
  `ctime` int(4) DEFAULT NULL,
  PRIMARY KEY (`dev_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_status`
--

LOCK TABLES `device_status` WRITE;
/*!40000 ALTER TABLE `device_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entry`
--

DROP TABLE IF EXISTS `entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry` (
  `entry_id` int(4) NOT NULL AUTO_INCREMENT,
  `entry_name` varchar(128) NOT NULL DEFAULT '',
  `domain` varchar(128) NOT NULL,
  `deploy_root` int(4) DEFAULT NULL,
  `ctime` int(4) NOT NULL,
  PRIMARY KEY (`entry_id`),
  UNIQUE KEY `key_0` (`entry_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry`
--

LOCK TABLES `entry` WRITE;
/*!40000 ALTER TABLE `entry` DISABLE KEYS */;
INSERT INTO `entry` VALUES (1,'api','api.qfpay.com',1,1458636072),(2,'qiantai2','qiantai2.qfpay.com',NULL,0);
/*!40000 ALTER TABLE `entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qfuser`
--

DROP TABLE IF EXISTS `qfuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qfuser` (
  `user_id` bigint(20) NOT NULL,
  `name` varchar(64) NOT NULL,
  `yc_uid` varchar(64) DEFAULT NULL,
  `bind_time` int(4) DEFAULT NULL,
  `tctime` int(4) NOT NULL,
  `event_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qfuser`
--

LOCK TABLES `qfuser` WRITE;
/*!40000 ALTER TABLE `qfuser` DISABLE KEYS */;
INSERT INTO `qfuser` VALUES (11751,'','E6dH0w6yHJtb/nnp31cAkg==',1460192936,1460019931,'1460192945.31yT6gBmP');
/*!40000 ALTER TABLE `qfuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_records`
--

DROP TABLE IF EXISTS `report_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report_records` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `deploy_id` int(4) NOT NULL,
  `time` varchar(16) NOT NULL,
  `record` varchar(512) DEFAULT NULL,
  `func_name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_records`
--

LOCK TABLES `report_records` WRITE;
/*!40000 ALTER TABLE `report_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_room`
--

DROP TABLE IF EXISTS `server_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_room` (
  `room_id` int(4) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(128) NOT NULL DEFAULT '',
  `code` varchar(64) NOT NULL,
  `intro` varchar(256) NOT NULL,
  `ctime` int(4) DEFAULT NULL,
  PRIMARY KEY (`room_id`),
  UNIQUE KEY `key_0` (`room_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_room`
--

LOCK TABLES `server_room` WRITE;
/*!40000 ALTER TABLE `server_room` DISABLE KEYS */;
INSERT INTO `server_room` VALUES (1,'北京','','蓝汛机房',1458640140);
/*!40000 ALTER TABLE `server_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service` (
  `service_id` int(4) NOT NULL AUTO_INCREMENT,
  `entry_id` int(4) NOT NULL,
  `service_name` varchar(128) NOT NULL DEFAULT '',
  `repos_name` varchar(256) NOT NULL,
  `intro` varchar(256) DEFAULT NULL,
  `rd` varchar(128) NOT NULL,
  `ctime` int(4) NOT NULL,
  PRIMARY KEY (`service_id`),
  UNIQUE KEY `key_0` (`service_name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,1,'marketing','',NULL,'',0),(2,0,'测试服务','git@git.qfpay.net:devops/sight.git','测试服务器','王帅',1460701441),(3,0,'','','','高建生',1460701660),(8,0,'yukykykykykyk','git@git.qfpay.net:devops/sight.git','','喻世俊',1460702969),(10,0,'rocky','iuiu','','高建生',1460703395),(11,0,'dfdfdfdf','dfdfdfdfdf','dfdfdfdfd','高建生',1460705350),(12,0,'fgregfgrhgfg','dfgdfgfdgfdfg','gdfgdeg','高建生',1460705475);
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_rel`
--

DROP TABLE IF EXISTS `service_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_rel` (
  `sr_id` int(4) NOT NULL AUTO_INCREMENT,
  `service_id1` int(2) NOT NULL,
  `service_id2` int(2) NOT NULL,
  `ctime` int(4) NOT NULL,
  PRIMARY KEY (`sr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_rel`
--

LOCK TABLES `service_rel` WRITE;
/*!40000 ALTER TABLE `service_rel` DISABLE KEYS */;
INSERT INTO `service_rel` VALUES (1,3,2,1458643026),(2,2,1,1458643059);
/*!40000 ALTER TABLE `service_rel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-18 22:04:21
