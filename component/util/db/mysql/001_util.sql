#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: 
# -- ---------------------------------------------
# -- Creating user small storage table.
# -- ---------------------------------------------

    CREATE TABLE `util_user_small_storage` (
	    `id` INT UNSIGNED NOT NULL,
	    `key` VARCHAR(32),
	    `data` VARBINARY(1024),
        `last_modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        `created_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
        PRIMARY KEY (`id`, `key`)
	) 
	ENGINE = InnoDB DEFAULT CHARSET=latin1;

# Downgrade your schema
DOWN:
# -- ---------------------------------------------
# -- Deleting table.
# -- ---------------------------------------------

    DROP TABLE IF EXISTS `util_user_small_storage`;
