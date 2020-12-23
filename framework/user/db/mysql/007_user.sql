#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: CREATE TABLE `user_accessgroup_info` (`externalid` VARCHAR(255) NOT NULL, `clienttype` INTEGER UNSIGNED NOT NULL, `groupname` VARCHAR(256) NOT NULL, PRIMARY KEY (`externalid`, `clienttype`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;

# Downgrade your schema
DOWN: DROP TABLE `user_accessgroup_info`;
