#
# Database migration script.  End each sql statement with a ;
#
# ----
# Note: Upgrading from 003 to 004 may fail due to the UNIQUE KEY `EXTERNAL`.  In that
#       case, you will need to manually intervene by running:
#
# ALTER TABLE `userinfo` CHANGE `externalid` `externalid` BIGINT(20) UNSIGNED;
# UPDATE `userinfo` SET `externalid` = NULL WHERE `externalid` = 0;
#
# Note: Also because of this, a downgrade from 005 to 004 may result in a failure. 
#       There is no real work-around for 005 to 004 because 004 requires a unique key
#       for externalid.  So DO NOT downgrade from 005 to 004 if you have PC users.
#
[MIGRATION]

# Upgrade your schema
UP:
    ALTER TABLE `userinfo` CHANGE `externalid` `externalid` BIGINT(20) UNSIGNED;
    UPDATE `userinfo` SET `externalid` = NULL WHERE `externalid` = 0;

# Downgrade your schema
DOWN:
    ALTER TABLE `userinfo` DISABLE KEYS;
    UPDATE `userinfo` SET `externalid` = 0 WHERE `externalid` = NULL;
    ALTER TABLE `userinfo` CHANGE `externalid` `externalid` BIGINT(20) UNSIGNED NOT NULL;
    ALTER TABLE `userinfo` ENABLE KEYS;

