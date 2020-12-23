import MySQLdb
from utils import *
from cmd import dumpinfo, upgrade, downgrade, create
import re

"""
 Validate the table names comply with the Blaze standards.
 framework - blaze_
 component - <component>_
"""
def validate_tables(cur, component, db):
  invalid = []
  pattern = re.compile('blaze_|%s_' % component, re.IGNORECASE)
  names = get_table_names(cur, db)
  for x in names:
    if pattern.match(x) is None:
      invalid.append('INVALID TABLE NAME %s FOR COMPONENT %s' % (x,component))

  return invalid

#
# test 
# -c<component> -d<db> -r<path> -v<version> -o<db options>
#
# component:  the component the script is for.
# db:         the database vendor, like mysql or oracle. 
# r:          root path, i.e trunk
# o:          db specific options to login.
# 
#
# This script will create a temporary schema and test a component.
#
def runcmd(component, cpath, db, root, version, dbopts):
  cur = None
  con = None
  try:
    con = get_con(dbopts)
    cur = con.cursor()
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    schema = create_test_schema(cur,component)
    info('Creating schema %s for testing...' % schema)

    # Override options
    dbopts['db'] = schema
    info('Upgrading component %s' % component)
    upgrade.runcmd(component,cpath,db,root,version,dbopts)

    # Validate
    invalid = validate_tables(cur,component,schema)
    if len(invalid) == 0:
        info('No invalid tables found')
    else:
        for t in invalid:
            warn(t)

    info('Downgrading component %s' % component)
    downgrade.runcmd(component,cpath,db,root,0,dbopts)
    info('Removing schema %s' % schema)
  except MySQLdb.Error, e:
    err('%d: %s' % (e.args[0], e.args[1]))
    con.rollback()
    raise DBError(ErrorCode.DB_ERROR, '%d: %s' % (e.args[0], e.args[1]))
  except MigError, me:
    err('Migration Error: %s' % me.errmsg)
    con.rollback()
    raise me
  finally:
    drop_schema(cur,schema)
    if cur:
      cur.close()
    if con:
      con.close()
