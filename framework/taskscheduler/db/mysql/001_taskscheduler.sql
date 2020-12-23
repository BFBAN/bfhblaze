#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: CREATE TABLE `task_scheduler` ( `task_id` int(10) unsigned NOT NULL auto_increment,`component_id` int(11) NOT NULL,`tdf_type` int(11) NOT NULL default '0', `tdf_raw` varbinary(4000) default NULL,`start` int(10) unsigned NOT NULL default '0',`duration` int(10) unsigned NOT NULL default '0',`recurrence` int(10) unsigned NOT NULL default '0',PRIMARY KEY  (`task_id`)) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

# Downgrade your schema
DOWN: DROP TABLE task_scheduler;
