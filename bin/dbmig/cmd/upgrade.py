import MySQLdb
from utils import *

#
# upgrade 
# -c<component> -d<db> -r<path> -v<version> -o<db options>
#
# component:  the component the script is for.
# db:         the database vendor, like mysql or oracle. 
# r:          root path, i.e trunk
# o:          db specific options to login.
#
# This script will upgrade a schema from one version to another, 
# either specified or latest.
#
# Once operations are completed, a fingerprint will be generated
# for the operation.
#
#
def runcmd(component, cpath, db, root, version, dbopts):
  cur = None
  con = get_con(dbopts)
  try:
    cur = con.cursor()
    check_version_table(cur, root)
    cur.execute('SELECT GET_LOCK(\'%s\',300);' % component)
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    [cur_ver,cur_fin] = get_current_version(cur, component)
    path = get_component_path(root, component, cpath)
    path = os.path.join(path,'db',db)
    print path

    script_exists = validate_scripts(component, path)
    if not script_exists:
      raise MigrationError(ErrorCode.NO_SCRIPTS_FOUND, 'Could not find a migration script matching NNN_%s.sql' % component)

    # Check integrity of current version
    if cur_ver > 0:
      sqlpath = find_migration(component, path, int(cur_ver))

      if sqlpath is None:
        raise MigrationError(ErrorCode.VERSION_FILE_MISSING,'Could not find a migration script that matches current version.  Please update your source.')
      sql = load_sql(sqlpath)
      finger = generate_fingerprint(sql)

      if finger != cur_fin:
        warn('The version in your source does not match the version in the database.')
          
    # Should we migrate?
    if cur_ver != version:
      ver = 1
      exists = True
    
      if cur_ver > 0:
        ver = cur_ver+1

      
      while exists:
        sqlpath = find_migration(component, path, ver)
        if sqlpath:
          info('Upgrading to version %d' % (ver-1))
          sql = load_sql(sqlpath)
          execute_sql(cur,component,ver,sql[0], generate_fingerprint(sql))
          con.commit()
          if version != 0 and version == ver:
            exists = False
          ver += 1
          info('Upgraded component %s to version %d' % (component, ver-1))
        else:
          exists = False

    else:
      info('Schema is up to date.')
    con.commit()
  except MySQLdb.Error, e:
    err('%d: %s' % (e.args[0], e.args[1]))
    con.rollback()
    raise DBError(ErrorCode.DB_ERROR, '%d: %s' % (e.args[0], e.args[1]))
  except MigError, me:
    con.rollback()
    raise me
  finally:
    cur.execute('SELECT RELEASE_LOCK(\'%s\');' % component)
    if cur:
      cur.close()
    if con:
      con.close()
