import MySQLdb
import sys, os, string, shutil, hashlib, getpass, time, glob
import ConfigParser
from socket import gethostname

"""
Migration Exception 

"""
class ErrorCode:
    INVALID_PARAMS = 900 #Input parameters were incorrect
    DB_CONF_MISSING = 1000 #Database configuration is missing
    DB_CONF_INVALID = 1001 #Database configuration is invalid
    DB_CONNECT_FAILURE = 1002 #Failed to connect to the database
    DB_SCHEMA_MISSING = 1003 #Failed to find schema template
    DB_ERROR = 1100 # General DB error
    VERSION_FILE_MISSING = 1200 # SQL script for version missing
    VERSION_MISMATCH = 1201 # local version and db version do not match
    NO_TABLES_FOUND = 1202 # No tables found to export
    NO_SCRIPTS_FOUND = 1203 # Couldn't find scripts to load

class MigError(Exception):
    def __init__(self,errno,errmsg):
        self.errno = errno
        self.errmsg = errmsg

class DatabaseConfigurationError(MigError): pass

class ParamError(MigError): pass

class DBError(MigError): pass

class MigrationError(MigError): pass
    

#
# info messages
#
def info(str):
    handle_msg('INFO',str)

def warn(str):
    handle_msg('WARN',str)

def err(str):
    handle_msg('ERROR',str)

#
# Handle messages
#
def handle_msg(level,message):
    print '[%s] %s' % (level, message)

#
# Retrieve a database connection
#
def get_con(opts):
    if opts is None:
        raise DatabaseConfigurationError(ErrorCode.DB_CONF_MISSING,'No database connection information')
    connection = None

    if not opts.has_key('host') or not opts.has_key('port') or not opts.has_key('user') or not opts.has_key('passwd') or not opts.has_key('db'):
        raise DatabaseConfigurationError(ErrorCode.DB_CONF_INVALID,'Invalid database configuration.')

    try:
        connection = MySQLdb.Connect(host=opts['host'], port=opts['port'],
            user=opts['user'], passwd=opts['passwd'],db=opts['db'])
    except MySQLdb.Error, e:
        raise DatabaseConfigurationError(ErrorCode.DB_CONNECT_FAILURE,'Failed to connect to database with error code %d' % (e.args[0]))
        
    return connection

#
# Parse a concatenated string; name=value,name2=value2,...
#
def parse_dbopts(opts):
    options = {}
    options['port'] = 3306
    s = opts.split(',')
    for x in s:
        tokens = x.split('=')
        if len(tokens) != 2:
            raise DatabaseConfigurationError(ErrorCode.DB_CONF_INVALID,'The database connection information is formatted improperly.')
        if tokens[0] == 'port':
            options[tokens[0]] = int(tokens[1])
        else:
            options[tokens[0]] = tokens[1]

    return options

#
# Construct SQL script name based on template.
#
def get_script_name(version, component):
    if version is None or component is None:
        raise ParamError(ErrorCode.INVALID_PARAMS,'Version or Component cannot be undefined.')
    fname = '%s_%s.sql' % (string.zfill(version,3),component)
    return fname

#
# Define path for migration file
# to it.
#
def get_migration_path(component, cpath, version):
    if version is None or component is None or cpath is None:
        raise ParamError(ErrorCode.INVALID_PARAMS,'Version,Component,or CPATH cannot be undefined.')
    fname = get_script_name(version,component)
    fpath = os.path.join(cpath,fname)
    return fpath

#
# Find a SQL script, if it exists, return the path
# to it.
#
def find_migration(component, cpath, version):
  fpath = get_migration_path(component, cpath, version)
  if os.path.exists(fpath):
    return fpath
  else:
    return None

#
# Check to see if any scripts exist.
#
def validate_scripts(component, cpath):
    scripts = glob.glob(os.path.join(cpath,'*_%s.sql' % component))
    if len(scripts) > 0:
        return True
    else:
        return False

"""
 Load a SQL script based on path
 Grab both UP and DOWN sections.
 [MIGRATION]
 VERSION: 2
 UP:
    STMT1;
    STMT2;
    PROC1;
 DOWN:
    STMT1;
    STMT2;
    PROC1;
"""
def load_sql(path):
  if os.path.exists(path):
    config = ConfigParser.ConfigParser()
    config.read(path)
    version = 1
    if config.has_option('MIGRATION','VERSION'):
        version = int(config.get('MIGRATION','VERSION'))

    up = config.get('MIGRATION','UP')
    down = config.get('MIGRATION','DOWN')
    delim = ';\n'

    if version > 1:
        delim = ';;'

    sql = [up.split(delim), down.split(delim)]

    return sql
  else:
    return None

#
# Validate that the version table exists
#
def check_version_table(cur, root):
  add = True
  try:
    cur.execute('select * from blaze_schema_info')
    res = cur.fetchall()
    add = False
  except MySQLdb.Error, e:
    warn('%d: %s' % (e.args[0], e.args[1]))
    info('Table blaze_schema_info is missing, attempting to add...')

  if add:
    sqlpath = os.path.join(root,'bin/dbmig/template/001_schemaversion.sql')
    sql = load_sql(sqlpath)
    if sql:
      for x in sql[0]:
        x = x.strip()
        if len(x) > 0:
          cur.execute(x)
      info('Table blaze_schema_info added.')
    else:
      raise DatabaseConfigurationError(ErrorCode.DB_SCHEMA_MISSING,'Failed to load schema version sql script from %s' % sqlpath)

#
# Retrieve the current version of a component
# in a database
#
def get_current_version(cur,component):
    if cur is None or component is None:
        raise ParamError(ErrorCode.INVALID_PARAMS,'Cursor and component cannot be empty')
    
    version = -1
    fingerprint = None
    cur.execute('select version, fingerprint from blaze_schema_info where component = \'%s\'' % component)
    res = cur.fetchone()
    if res:
        version = res[0]
        fingerprint = res[1]
    return [int(version),fingerprint]

#
# Generate a fingerprint for a sql script.
# This can be used to indentify out of sync issues.
#
def generate_fingerprint(sql):
    str = ''
    if sql:
        for y in sql:
            for x in y:
                x = x.strip()
                if len(x) > 0:
                    str+=x
    m = hashlib.md5()
    m.update(str)
    m.digest()
    return m.hexdigest()

#
# Execute SQL statements in a given script.
# Once completed, update the fingerprint.
#
def execute_sql(cur,component,version,sql,finger):
    # Execute sql
    for x in sql:
        x = x.strip()
        if len(x) > 0:
            info('Executing %s' % x)
            cur.execute(x)
  
    set_version(cur, component, version, finger)

#
# Set the version of a component
#
def set_version(cur, component, version, finger):
    hname = gethostname()
    if cur is None or component is None or version is None or finger is None:
        raise ParamError(ErrorCode.INVALID_PARAMS,'Cursor, component, version, or fingerprint cannot be empty')

    # No longer in db, remove the entry
    if version == 0:
        cur.execute('delete from blaze_schema_info where component = \'%s\'' % component)
    else:
        # Set version
        cur.execute('select component, version, last_updated, fingerprint, notes from blaze_schema_info where component = \'%s\'' % component)
        res = cur.fetchone()
    # update version
        if res:
            cur.execute('update blaze_schema_info set version = %d, last_updated = now(), fingerprint = \'%s\', notes = \'%s\' where component = \'%s\'' % (version, finger, hname, component))
    # version didn't exist so add it in
        else:
            cur.execute('insert into blaze_schema_info (component, version, last_updated, fingerprint, notes) values (\'%s\',%d,now(),\'%s\',\'%s\')' % (component, version, finger,hname))

#
# Create the template file
# If we have SQL statements to issue, then dump them to the file.
#
def write_sql_file(root, fpath, upstmt, downstmt):
  if len(upstmt) > 0 and len(downstmt) > 0:
    template = open(os.path.join(root,'bin/dbmig/template/00N_component.sql'),'r')
    output = open(fpath,'w')

    for line in template.readlines():
      output.write(line)
      if line.find('UPGRADE') > 0:
        for u in upstmt:
          output.write(' '+u)
      elif line.find('DOWNGRADE') > 0:
        for d in downstmt:
          output.write(' '+d)
    template.close()
    output.close()
  else:
    shutil.copyfile(os.path.join(root,'bin/dbmig/template/00N_component.sql'),fpath)


#
# Retrieve a list of tables in a schema
#
def get_table_names(cur, dbname):
  tables = []
  #cur.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \'%s\' ORDER BY CREATE_TIME DESC' % dbname)
  cur.execute('SHOW TABLES FROM %s' % dbname)
  res = cur.fetchall()
  for x in res:
	if x[0] != 'blaze_schema_info':
		tables.append(x[0])
  return tables

#
# Retrieve table information
#
def get_table_sql(cur,table):
  cur.execute('show create table `%s`' % table)
  res = cur.fetchone()
  sql = res[1]
  sql = sql.replace('\n','')
  sql = sql.strip()

  return sql

#
# Retrieve a list if procedures
#
def get_proc_names(cur, dbname):
    procs = []
    cur.execute('SELECT ROUTINE_NAME, ROUTINE_DEFINITION FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_SCHEMA = \'%s\' and ROUTINE_TYPE = \'PROCEDURE\'' % dbname)
    res = cur.fetchall()
    procs = []
    for x in res:
        procs.append([x[0],x[1].replace('\r\n',' ').replace('  ','')])
    return procs
#
# Retrieve the path to a component
#
def get_component_path(root, component, cpath):
  if cpath is None:
    return os.path.join(root,component)
  else:
    return os.path.join(root,cpath)

"""
 Create a schema

"""
def create_schema(cur,schema):
  cur.execute('CREATE SCHEMA %s' % schema)

def drop_schema(cur, schema):
  cur.execute('DROP SCHEMA %s' % schema)

"""
 Create a test schema
 Creates a schema for testing purposes using
 the formate user_component_time
"""
def create_test_schema(cur,component):
    user = getpass.getuser()
    t = time.strftime('%m%d%Y%H%M%S')
    schema = '%s_%s_%s' % (user, component, t)
    info(schema)
    create_schema(cur,schema)
    return schema
