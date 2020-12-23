#
# Database migration script.  End each sql statement with a ;
#
[MIGRATION]

# Upgrade your schema
UP: 
          ALTER TABLE `userinfo` MODIFY `persona` VARCHAR(32); 
          ALTER TABLE `userinfo` MODIFY `canonicalpersona` VARCHAR(32); 

# Downgrade your schema
DOWN: 
          DELETE FROM userinfo WHERE personaid < 0; 
          ALTER TABLE `userinfo` MODIFY `persona` VARCHAR(32) NOT NULL; 
          ALTER TABLE `userinfo` MODIFY `canonicalpersona` VARCHAR(32) NOT NULL; 

