#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: 
	ALTER TABLE `userinfo` ADD COLUMN `status` int(10) default 1;

# Downgrade your schema
DOWN: 
	ALTER TABLE `userinfo` DROP COLUMN `status`;

