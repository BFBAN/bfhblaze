#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP:
    ALTER TABLE `userinfo` ADD COLUMN `canonicalpersona` VARCHAR(32)  NOT NULL AFTER `persona`;
    UPDATE userinfo SET canonicalpersona=LOWER(REPLACE(persona,' ',''));

# Downgrade your schema
DOWN:
    ALTER TABLE `userinfo` DROP COLUMN `canonicalpersona`;

