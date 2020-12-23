import MySQLdb
from utils import *

#
# downgrade 
# -c<component> -d<db> -r<path> -v<version> -o<db options>
#
# component:  the component the script is for.
# db:         the database vendor, like mysql or oracle. 
# r:          root path, i.e trunk
# o:          db specific options to login.
#
# This script will downgrade a schema from one version to another.
#
# Once operations are completed, a fingerprint will be generated
# for the operation.
#
def runcmd(component, cpath, db, root, version, dbopts):
  cur = None
  con = None
  try:
    con = get_con(dbopts)
    cur = con.cursor()
    check_version_table(cur, root)
    cur.execute('SELECT GET_LOCK(\'%s\',300);' % component)
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    [cur_ver,cur_fin] = get_current_version(cur, component)
    path = get_component_path(root,component,cpath)
    path = os.path.join(path,'db',db)

    script_exists = validate_scripts(component, path)
    if not script_exists:
      raise MigrationError(ErrorCode.NO_SCRIPTS_FOUND, 'Could not find a migration script matching NNN_%s.sql' % component)

    # Check integrity of current version
    if cur_ver > 0:
      sqlpath = find_migration(component, path, cur_ver)
      if sqlpath is None:
        raise MigrationError(ErrorCode.VERSION_FILE_MISSING,'Could not find a migration script that matches current version.  Please update your source.')

      sql = load_sql(sqlpath)
      finger = generate_fingerprint(sql)

      if finger != cur_fin:
        warn('The version in your source does not match the version in the database.')

    if cur_ver > version:
      ver = cur_ver
      exists = True
    
      while exists and ver > version:
        sqlpath = find_migration(component, path, ver)
        sqlpath_prev = find_migration(component, path, ver-1)
        if sqlpath:
          info('Downgrading to version %d' % (ver))
          sql = load_sql(sqlpath)
          sql2 = None
          if sqlpath_prev:
            sql2 = load_sql(sqlpath_prev)
          execute_sql(cur,component,ver-1,sql[1],generate_fingerprint(sql2))
          ver -= 1
          info('Downgraded component %s to version %d' % (component, ver))
        else:
          exists = False
    else:
      info('Schema is up to date.')

    con.commit()
  except MySQLdb.Error, e:
    err('%d: %s' % (e.args[0], e.args[1]))
    con.rollback()
    raise DBError(ErrorCode.DB_ERROR,'%d: %s' % (e.args[0], e.args[1]))
  except MigError, me:
    con.rollback()
    raise me
  finally:
    cur.execute('SELECT RELEASE_LOCK(\'%s\');' % component)
    if cur:
      cur.close()
    if con:
      con.close()
