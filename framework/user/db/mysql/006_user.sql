#
# Database migration script.  End each sql statement with a ;
#
# ----
#
[MIGRATION]

# Upgrade your schema
UP:
    ALTER TABLE `userinfo` 
        ADD COLUMN `accountlocale` INTEGER UNSIGNED NOT NULL DEFAULT 0 AFTER `persona`;

# Downgrade your schema
DOWN:
    ALTER TABLE `userinfo` DROP COLUMN `accountlocale`;
