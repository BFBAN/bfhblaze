#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP:
    ALTER TABLE `userinfo` ADD INDEX `canonicalpersona_idx` (`canonicalpersona`);

# Downgrade your schema
DOWN:
    ALTER TABLE `userinfo` DROP INDEX `canonicalpersona_idx`;

