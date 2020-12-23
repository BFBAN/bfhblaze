#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: CREATE TABLE `userinfo` ( `blazeid` int(10) unsigned NOT NULL auto_increment,`nucleusid` bigint(20) NOT NULL,`personaid` bigint(20) default NULL, `email` varchar(256) NOT NULL, `persona` varchar(32) NOT NULL, `externalid` bigint(20) unsigned NOT NULL, PRIMARY KEY  (`blazeid`), UNIQUE KEY `PERSONA` USING BTREE (`personaid`), KEY `EXTERNAL` (`externalid`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;

# Downgrade your schema
DOWN: DROP TABLE userinfo;
