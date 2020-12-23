import MySQLdb
import utils
from utils import *

#
# Creates a new migration script to run.
#
# create -c<component> -d<db> -r<path>
# component:  the component the script is for.
# db:         the database vendor, like mysql or oracle. 
# r:          root path, i.e trunk
#
# This command will attempt to generate a sql template
# script for a given command.  It will label the sql
# script as 00N, where N is the next highest value.
#
# Each script contains an UP and DOWN section.  UP
# is to be used for upgrading a schema, DOWN will be
# used to downgrade a schema.
#
#
def runcmd(component, cpath, db, root, dbopts, tables):
  path = get_component_path(root, component, cpath)

  # If component doesn't exist, halt
  if os.path.exists(path) is False:
    raise ParamError(ErrorCode.INVALID_PARAMS,'The component path %s does not exist.' % path)
  # see if a db dir exists, if not create one
  else:
    path = os.path.join(path,'db',db)

    if os.path.exists(path) is False:
      os.makedirs(path)
  # scripts follow the form 001_component.sql
  i = 1
  exists = True
  # While a 00N_component.sql script exists, increment N
  # until we find an available one.
  while exists:
    fpath = find_migration(component, path, i)
    if fpath:
      i+=1
    else:
      exists = False

  # Create a new template file
  fpath = get_migration_path(component, path, i)

  upstmt = []
  downstmt = []

  if dbopts and tables:
    cur = None
    con = None
    try:
      con = get_con(dbopts)
      cur = con.cursor()
      check_version_table(cur, root)
      tab = []
      """
      Grab tables
      """
      if tables == '*':
        tab = get_table_names(cur,dbopts['db'])
      else:
        tab = tables.split(',')

      if tab is None or len(tab) == 0:
        raise MigrationError(ErrorCode.NO_TABLES_FOUND,'No tables found to migrate')
      else:
        for t in tab:
          upstmt.append(get_table_sql(cur,t)+';\n')
          downstmt.append('DROP TABLE %s;\n' % t)
      """
      Grab stored procedues
      """
      procs = get_proc_names(cur,dbopts['db'])
      if procs is None or len(procs) == 0:
        info('No procedures found')
      else:
        for x in procs:
            upstmt.append('CREATE PROCEDURE %s() %s;\n' % (x[0],x[1]))
            downstmt.append('DROP PROCEDURE %s;\n' % (x[0]))
      write_sql_file(root, fpath, upstmt, downstmt)
      if len(upstmt) > 0 and len(downstmt) > 0:
        finger = generate_fingerprint(load_sql(fpath))
        set_version(cur, component, i, finger)
        con.commit()
    except MySQLdb.Error, e:
      err('%d: %s' % (e.args[0], e.args[1]))
      raise DBError(ErrorCode.DB_ERROR,'%d: %s' % (e.args[0], e.args[1]))
    except MigError, me:
      raise me
    finally:
      if cur:
        cur.close()
      if con:
        con.close()
  else:
    write_sql_file(root, fpath, upstmt, downstmt)

  info('Created migration file at %s' % fpath)
