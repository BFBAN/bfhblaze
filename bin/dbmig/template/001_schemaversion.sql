#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP:
  CREATE TABLE IF NOT EXISTS `blaze_schema_info` ( 
    `component` VARCHAR(64) NOT NULL, 
    `version` NUMERIC UNSIGNED NOT NULL, 
    `last_updated` DATETIME NOT NULL, 
    `fingerprint` VARCHAR(255) NOT NULL, 
    `notes` VARCHAR(255) NOT NULL, 
    PRIMARY KEY (`component`) 
  ) 
  ENGINE = InnoDB; 

  INSERT into `blaze_schema_info` values ('version',1,NOW(),'1234','Initial version');

# INSERT YOUR UPGRADE STATEMENTS HERE

# Downgrade your schema
DOWN:
# INSERT YOUR DOWNGRADE STATEMENTS HERE
