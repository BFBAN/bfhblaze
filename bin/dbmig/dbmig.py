#!/opt/local/bin/python

#/usr/bin/env python2.5
"""
 DB Migration

 Script to help manage database schemas and versioning of them.
 The basic principle is that as you iterate through code
 SQL Scripts:
 <component>/db/<vendor>/001_script.sql
 
 TODO
 ----
 - Incorporate into CI.
 - Using host=localhost fails on certain hosts
 - Add check-version option to validate that the current tables are up to date.
 - Add oracle support
 - Add config version header

 06.26.08
 * Added a check for MySQLdb module.  If not present, output a warning.

 05.06.08
 * Added parameters to allow custom username,password,catalogs for adduser command

 04.17.08
 * Added option to create user and space

 04.07.08
 * Removed -t flag.
 * Fix database options param from string to a structure
 * Add table locking for concurrency support

 04.02.08
 * Added warning about using -t flag.
 * Add support for stored procedures
 * Add cursor checks

 03.27.08
 * Unit tests.
 * Test schema defined.
 * Added error codes
 * Fixed invalid parameter error.
 * Hostnames are now logged as part of updates.
 * Resolved an error where foreign keys intefered with upgrades.

 09.11.07
 * Adding support to define component path 

 08.29.07:
 * Create package and crude command structure.

 08.28.07:
 * Resolved linux support.
 * Added support to generate scripts from schema.
"""
import sys, os, string, shutil, hashlib
from optparse import OptionParser
from getpass import *

try:
    import MySQLdb
except ImportError:
    print 'Modules failed to import properly. This is likely to do with your Python path settings.  Please run setenv.'
    sys.exit(1)

from utils import *
from cmd import dumpinfo, upgrade, downgrade, create, test, adduser

#
# Option wrapper
#
class DbMigOptionParser(OptionParser):
  def print_usage_and_exit(self):
    self.print_help(sys.stderr)
    sys.exit(1)

ACTION_MAPPING = {
  'create':create,
  'upgrade':upgrade,
  'downgrade':downgrade,
  'info':dumpinfo,
  'test':test,
  'adduser':adduser
}

#
# Main driver
#
def main(argv):
  if argv is None:
    argv = sys.argv
  #
  # Define command line parameters and usage
  #
  usage = "usage: %prog action [options]"
  version = "DB Migration 1.0"
  parser = DbMigOptionParser(usage=usage, version=version)
  parser.add_option('-c','--component',dest='component',
    metavar='COMPONENT',help='COMPONENT configuring.')
  parser.add_option('--cpath',dest='cpath',
    metavar='COMPONENT_PATH',help='COMPONENT_PATH is the path to a component.')
  parser.add_option('-d','--database',dest='db',
    metavar='DATABASE',help='DATABASE to connect to.')
  parser.add_option('-r','--root',dest='root',
    metavar='PATH',help='PATH to root of trunk.')
  parser.add_option('-V','--SVERSION',dest='version',type='int',
    metavar='VERSION',help='VERSION to update to.')
  parser.add_option('-o','--options',dest='dbopts',
    metavar='OPTIONS',help='OPTIONS specific to a database.')
  parser.add_option('-t','--test',dest='test',action='store_true',
    help='Do not commit changes.')
  parser.add_option('--tables',dest='tables',
    help='Tables to create migration scripts for.')
  parser.add_option('--user',dest='user',
    help='Username to create.');
  parser.add_option('--password',dest='password',
    help='Password to set.');

  (options, args) = parser.parse_args(argv[1:])

  try:
    action = args[0]
  except IndexError:
    parser.print_usage_and_exit()

  if options.test:
    err('-t is not supported at this time as databases do not allow CREATE,ALTER, or DROP statements from being rolled back.  Please test against a test data set')
    sys.exit(1)

  try:
    if action == 'create':
      if options.component and options.db and options.root and options.cpath and options.dbopts and options.tables:
        ACTION_MAPPING[action].runcmd(options.component, options.cpath, options.db, options.root, parse_dbopts(options.dbopts), options.tables)
      elif options.component and options.db and options.root and options.cpath:
        ACTION_MAPPING[action].runcmd(options.component, options.cpath, options.db, options.root, None, None)
      else:
        info('-c: %s'%options.component)
        info('-r: %s'%options.root)
        info('--cpath: %s'%options.cpath)
        info('-d: %s'%options.db)
        info('-o: %s'%options.dbopts)
        info('--tables: %s'%options.tables)
        raise ParamError(ErrorCode.INVALID_PARAMS,'Missing parameters')
    elif action == 'upgrade':
      if options.component and options.db and options.root and options.dbopts and options.cpath:
        ACTION_MAPPING[action].runcmd(options.component, options.cpath, options.db, options.root, options.version, parse_dbopts(options.dbopts))
      else:
        info('-c: %s'%options.component)
        info('-r: %s'%options.root)
        info('-d: %s'%options.db)
        info('-o: %s'%options.dbopts)
        info('--cpath: %s'%options.cpath)
        info('-V: %s'%options.version)
        raise ParamError(ErrorCode.INVALID_PARAMS,'Missing parameters')
    elif action == 'downgrade':
      if options.component and options.db and options.root and options.dbopts:
        if options.version < 0:
          print 'Version missing.'
        else:
          ACTION_MAPPING[action].runcmd(options.component, options.cpath, options.db, options.root, options.version, parse_dbopts(options.dbopts))
    elif action == 'test':
      if options.component and options.db and options.root and options.dbopts and options.cpath:
        ACTION_MAPPING[action].runcmd(options.component, options.cpath, options.db, options.root, options.version, parse_dbopts(options.dbopts))
      else:
        info('-c: %s'%options.component)
        info('-r: %s'%options.root)
        info('-d: %s'%options.db)
        info('-o: %s'%options.dbopts)
        info('--cpath: %s'%options.cpath)
        info('-V: %s'%options.version)
        raise ParamError(ErrorCode.INVALID_PARAMS,'Missing parameters')
    elif action == 'info':
      if options.dbopts:
          ACTION_MAPPING[action].runcmd(parse_dbopts(options.dbopts))
      else:
        info('-o: %s'%options.dbopts)
        raise ParamError(ErrorCode.INVALID_PARAMS,'Missing parameters')
    elif action == 'adduser':
      if options.dbopts:
          user = options.user
          password = options.password
          db = options.db
          if user is None:
            user = getuser()
          if password is None:
            password = user
          if db is None:
            db = user
          ACTION_MAPPING[action].runcmd(parse_dbopts(options.dbopts),user,password,db)
      else:
        info('-o: %s'%options.dbopts)
        raise ParamError(ErrorCode.INVALID_PARAMS,'Missing parameters')
  except MigError, me:
      err('Migration Error: (%d) %s' % (me.errno,me.errmsg))
    
if __name__ == '__main__':
  main(sys.argv)
