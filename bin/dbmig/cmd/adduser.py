import MySQLdb
import utils
from utils import *

#
# adduser
# -o<db options>
# -u <username>
#
# o:        db specific options to login.
# u:        username to add
#
# creates a test account
#
def runcmd(dbopts, user, passwd, dbname):
  con = None
  cur = None

  try:
    con = get_con(dbopts)
    cur = con.cursor()
    cur.execute('show databases like \'%s\'' % dbname)
    res = cur.fetchall()
    if len(res) == 0:
        cur.execute('create database %s' % dbname)
    else:
        info('Database %s already exists.' % dbname)
    cur.execute('grant all privileges on %s.* to \'%s\'@\'%%\' identified by \'%s\' with grant option' % (dbname, user, passwd))
    print 'Created account for %s' % user
  except MySQLdb.Error, e:
    err('%d: %s' % (e.args[0], e.args[1]))
    con.rollback()
    raise DBError(ErrorCode.DB_ERROR, '%d: %s' % (e.args[0], e.args[1]))
  except MigError, me:
    err('Migration Error: %s' % me.errmsg)
    raise me
  finally:
    if cur:
      cur.close()
    if con:
      con.close()
