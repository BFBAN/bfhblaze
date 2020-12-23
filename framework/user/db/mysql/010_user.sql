#
# Database migration script.  End each sql statement with a ;
#
# ----
#
[MIGRATION]

# Upgrade your schema
UP:
    ALTER TABLE `userinfo` ADD COLUMN `externalblob` BINARY(36) DEFAULT NULL COMMENT 'sizeof(SceNpId)==36' AFTER `externalid`;

# Downgrade your schema
DOWN:
    ALTER TABLE `userinfo` DROP COLUMN `externalblob`;
