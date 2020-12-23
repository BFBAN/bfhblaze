#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: 
	CREATE TABLE `blazemetrics` (`BLAZEID` int(10) unsigned NOT NULL default '0',`SERVICENAME` varchar(50) NOT NULL,`ACCOUNTUID` varchar(50) NOT NULL,`PERSONAUID` varchar(50) NOT NULL,`COUNTRYCODE` varchar(8) NOT NULL,`MAC` varchar(34) NOT NULL,`AGE` int(10) unsigned NOT NULL,`GENDER` varchar(1) NOT NULL,`UPSTREAM` int(10) unsigned NOT NULL,`DOWNSTREAM` int(10) unsigned NOT NULL,`NATTYPE` int(10) unsigned default NULL,`UPNP` varchar(20) default NULL,`ROUTERINFO` varchar(128) default NULL,`TOTSESSIONTIME` bigint(20) unsigned NOT NULL,`TOTSESSIONCOUNT` int(10) unsigned NOT NULL,`TIMESINCELASTAUTH` bigint(20) unsigned NOT NULL,`AUTHDATETIME` datetime NOT NULL,`CREATEDATE` datetime NOT NULL,`UPDATEDATE` datetime NOT NULL,PRIMARY KEY  (`BLAZEID`),UNIQUE KEY `UNIQUE_KEY` (`BLAZEID`),KEY `CREATEDATE_INDEX` (`CREATEDATE`),KEY `UPDATEDATE_INDEX` (`UPDATEDATE`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	CREATE TABLE `blazemetrics_ping` (`BLAZEID` int(10) unsigned NOT NULL default '0',`PINGHOST` varchar(100) NOT NULL,`PINGVALUE` int(11) NOT NULL,`SERVICENAME` varchar(50) NOT NULL,PRIMARY KEY  USING BTREE (`BLAZEID`,`PINGHOST`),UNIQUE KEY `UNIQUE_KEY` (`BLAZEID`,`PINGHOST`),CONSTRAINT `FK_blazemetrics_ping_1` FOREIGN KEY (`BLAZEID`) REFERENCES `blazemetrics` (`BLAZEID`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='InnoDB free: 1270784 kB; (`LOGINID`) REFER `blaze_metrics/me';
	CREATE TABLE `blazemetrics_mac` (`MAC` varchar(34) NOT NULL,`SINCE` datetime NOT NULL,`LASTAUTH` datetime NOT NULL,PRIMARY KEY  (`MAC`),UNIQUE KEY `UNIQUE_KEY` (`MAC`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# Downgrade your schema
DOWN: 
	DROP TABLE IF EXISTS `blazemetrics_ping`;
	DROP TABLE IF EXISTS `blazemetrics`;
	DROP TABLE IF EXISTS `blazemetrics_mac`;
