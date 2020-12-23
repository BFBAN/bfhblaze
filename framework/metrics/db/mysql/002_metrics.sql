#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: 
      DROP TABLE IF EXISTS `blazemetrics`;
      CREATE TABLE  `blazemetrics` (`BLAZEID` int(10) unsigned NOT NULL default '0',`ACCOUNTUID` varchar(64) NOT NULL,`PERSONAUID` varchar(64) NOT NULL,`COUNTRYCODE` int(10) unsigned NOT NULL,`MAC` varchar(34) default NULL,`AGE` int(10) unsigned default NULL,`GENDER` varchar(1) default NULL,`UPSTREAM` bigint(20) unsigned default '0',`DOWNSTREAM` bigint(20) unsigned default '0',`NATTYPE` int(10) unsigned default NULL,`UPNP` tinyint(1) default '0',`ROUTERINFO` varchar(128) default NULL,`TOTSESSIONTIME` bigint(20) unsigned NOT NULL,`TOTSESSIONCOUNT` int(10) unsigned NOT NULL,`TIMESINCELASTAUTH` bigint(20) unsigned NOT NULL,`AUTHDATETIME` datetime NOT NULL,`CREATEDATE` datetime NOT NULL,`UPDATEDATE` datetime NOT NULL,PRIMARY KEY  (`BLAZEID`),UNIQUE KEY `UNIQUE_KEY` (`BLAZEID`),KEY `CREATEDATE_INDEX` (`CREATEDATE`),KEY `UPDATEDATE_INDEX` (`UPDATEDATE`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;
      DROP TABLE IF EXISTS `blazemetrics_mac`;
      CREATE TABLE  `blazemetrics_mac` (`MAC` varchar(34) NOT NULL,`SINCE` datetime NOT NULL,`LASTAUTH` datetime NOT NULL,PRIMARY KEY  (`MAC`),UNIQUE KEY `UNIQUE_KEY` (`MAC`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;
      DROP TABLE IF EXISTS `blazemetrics_ping`;
      CREATE TABLE  `blazemetrics_ping` (`BLAZEID` int(10) unsigned NOT NULL default '0',`PINGHOST` varchar(100) NOT NULL,`PINGVALUE` int(11) NOT NULL,PRIMARY KEY  USING BTREE (`BLAZEID`,`PINGHOST`),UNIQUE KEY `UNIQUE_KEY` (`BLAZEID`,`PINGHOST`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='InnoDB free: 1270784 kB; (`LOGINID`) REFER `blaze_metrics/me';

# Downgrade your schema
DOWN: 
	DROP TABLE IF EXISTS `blazemetrics_ping`;
	DROP TABLE IF EXISTS `blazemetrics`;
	DROP TABLE IF EXISTS `blazemetrics_mac`;
