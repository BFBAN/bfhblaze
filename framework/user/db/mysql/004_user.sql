#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP:
    ALTER TABLE `userinfo` DROP INDEX `canonicalpersona_idx`;
    ALTER TABLE `userinfo` ADD UNIQUE KEY `canonicalpersona_idx` USING BTREE (`canonicalpersona`);
    ALTER TABLE `userinfo` DROP KEY `EXTERNAL`;
    ALTER TABLE `userinfo` ADD UNIQUE KEY `EXTERNAL` (`externalid`);

# Downgrade your schema
DOWN:
    ALTER TABLE `userinfo` DROP INDEX `canonicalpersona_idx`;
    ALTER TABLE `userinfo` ADD INDEX `canonicalpersona_idx` (`canonicalpersona`);
    ALTER TABLE `userinfo` DROP KEY `EXTERNAL`;
    ALTER TABLE `userinfo` ADD KEY `EXTERNAL` (`externalid`);

