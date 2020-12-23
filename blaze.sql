/*
Navicat MySQL Data Transfer

Source Server         : EA
Source Server Version : 50140
Source Host           : 127.0.0.1:3306
Source Database       : qos

Target Server Type    : MYSQL
Target Server Version : 50140
File Encoding         : 65001

Date: 2013-09-07 10:31:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for blazemetrics
-- ----------------------------
DROP TABLE IF EXISTS `blazemetrics`;
CREATE TABLE `blazemetrics` (
  `BLAZEID` int(10) unsigned NOT NULL DEFAULT '0',
  `ACCOUNTUID` varchar(64) NOT NULL,
  `PERSONAUID` varchar(64) NOT NULL,
  `COUNTRYCODE` int(10) unsigned NOT NULL,
  `MAC` varchar(34) DEFAULT NULL,
  `AGE` int(10) unsigned DEFAULT NULL,
  `GENDER` varchar(1) DEFAULT NULL,
  `UPSTREAM` bigint(20) unsigned DEFAULT '0',
  `DOWNSTREAM` bigint(20) unsigned DEFAULT '0',
  `NATTYPE` int(10) unsigned DEFAULT NULL,
  `UPNP` tinyint(1) DEFAULT '0',
  `ROUTERINFO` varchar(128) DEFAULT NULL,
  `TOTSESSIONTIME` bigint(20) unsigned NOT NULL,
  `TOTSESSIONCOUNT` int(10) unsigned NOT NULL,
  `TIMESINCELASTAUTH` bigint(20) unsigned NOT NULL,
  `AUTHDATETIME` datetime NOT NULL,
  `CREATEDATE` datetime NOT NULL,
  `UPDATEDATE` datetime NOT NULL,
  PRIMARY KEY (`BLAZEID`),
  UNIQUE KEY `UNIQUE_KEY` (`BLAZEID`),
  KEY `CREATEDATE_INDEX` (`CREATEDATE`),
  KEY `UPDATEDATE_INDEX` (`UPDATEDATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of blazemetrics
-- ----------------------------

-- ----------------------------
-- Table structure for blazemetrics_mac
-- ----------------------------
DROP TABLE IF EXISTS `blazemetrics_mac`;
CREATE TABLE `blazemetrics_mac` (
  `MAC` varchar(34) NOT NULL,
  `SINCE` datetime NOT NULL,
  `LASTAUTH` datetime NOT NULL,
  PRIMARY KEY (`MAC`),
  UNIQUE KEY `UNIQUE_KEY` (`MAC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of blazemetrics_mac
-- ----------------------------

-- ----------------------------
-- Table structure for blazemetrics_ping
-- ----------------------------
DROP TABLE IF EXISTS `blazemetrics_ping`;
CREATE TABLE `blazemetrics_ping` (
  `BLAZEID` int(10) unsigned NOT NULL DEFAULT '0',
  `PINGHOST` varchar(100) NOT NULL,
  `PINGVALUE` int(11) NOT NULL,
  PRIMARY KEY (`BLAZEID`,`PINGHOST`) USING BTREE,
  UNIQUE KEY `UNIQUE_KEY` (`BLAZEID`,`PINGHOST`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='InnoDB free: 1270784 kB; (`LOGINID`) REFER `blaze_metrics/me';

-- ----------------------------
-- Records of blazemetrics_ping
-- ----------------------------

-- ----------------------------
-- Table structure for blaze_schema_info
-- ----------------------------
DROP TABLE IF EXISTS `blaze_schema_info`;
CREATE TABLE `blaze_schema_info` (
  `component` varchar(64) NOT NULL,
  `version` decimal(10,0) unsigned NOT NULL,
  `last_updated` datetime NOT NULL,
  `fingerprint` varchar(255) NOT NULL,
  `notes` varchar(255) NOT NULL,
  PRIMARY KEY (`component`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of blaze_schema_info
-- ----------------------------
INSERT INTO `blaze_schema_info` VALUES ('metrics', '2', '2010-11-09 13:21:30', 'd3c8eac6042c82104d1f25d93aa336ff', 'gosprod-qos01.m3d-dfw.ea.com');
INSERT INTO `blaze_schema_info` VALUES ('taskscheduler', '1', '2010-11-09 13:21:29', '09674c5c05ad38e2fd83f5c5d0169025', 'gosprod-qos01.m3d-dfw.ea.com');
INSERT INTO `blaze_schema_info` VALUES ('user', '10', '2010-11-09 13:21:29', '1fe53eb54af4cbb11e49f5b8fecfdb7a', 'gosprod-qos01.m3d-dfw.ea.com');
INSERT INTO `blaze_schema_info` VALUES ('version', '1', '2010-11-09 13:21:28', '1234', 'Initial version');

-- ----------------------------
-- Table structure for task_scheduler
-- ----------------------------
DROP TABLE IF EXISTS `task_scheduler`;
CREATE TABLE `task_scheduler` (
  `task_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `component_id` int(11) NOT NULL,
  `tdf_type` int(11) NOT NULL DEFAULT '0',
  `tdf_raw` varbinary(4000) DEFAULT NULL,
  `start` int(10) unsigned NOT NULL DEFAULT '0',
  `duration` int(10) unsigned NOT NULL DEFAULT '0',
  `recurrence` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of task_scheduler
-- ----------------------------

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `blazeid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nucleusid` bigint(20) NOT NULL,
  `personaid` bigint(20) DEFAULT NULL,
  `email` varchar(256) NOT NULL,
  `persona` varchar(32) DEFAULT NULL,
  `accountlocale` int(10) unsigned NOT NULL DEFAULT '0',
  `canonicalpersona` varchar(32) DEFAULT NULL,
  `externalid` bigint(20) unsigned DEFAULT NULL,
  `externalblob` binary(36) DEFAULT NULL COMMENT 'sizeof(SceNpId)==36',
  `status` int(10) DEFAULT '1',
  PRIMARY KEY (`blazeid`),
  UNIQUE KEY `canonicalpersona_idx` (`canonicalpersona`) USING BTREE,
  UNIQUE KEY `EXTERNAL` (`externalid`),
  UNIQUE KEY `PERSONA` (`personaid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of userinfo
-- ----------------------------

-- ----------------------------
-- Table structure for user_accessgroup_info
-- ----------------------------
DROP TABLE IF EXISTS `user_accessgroup_info`;
CREATE TABLE `user_accessgroup_info` (
  `externalid` varchar(255) NOT NULL,
  `clienttype` int(10) unsigned NOT NULL,
  `groupname` varchar(256) NOT NULL,
  PRIMARY KEY (`externalid`,`clienttype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of user_accessgroup_info
-- ----------------------------
