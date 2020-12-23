import MySQLdb
import utils
from utils import DBError, MigError, ErrorCode

#
# info
# -o<db options>
#
# o:        db specific options to login.
#
# Dump schema version information to command line.
#
#
def runcmd(dbopts):
  con = None
  cur = None
  try:
    con = utils.get_con(dbopts)
    cur = con.cursor()
    cur.execute('select component, version, last_updated, fingerprint from blaze_schema_info')
    res = cur.fetchall()

    print ''
    print '%s|%s|%s|%s' % ('Component'.ljust(15), 'Last Updated'.ljust(20), 'Version'.ljust(7), 'Fingerprint'.ljust(30))
    print '%s|%s|%s|%s' % ('-'.ljust(15,'-'), '-'.ljust(20,'-'), '-'.ljust(7,'-'), '-'.ljust(30,'-'))

    for x in res:
      print '%s|%s|%s|%s' % (x[0].ljust(15), x[2].strftime("%m/%d/%y %H:%M:%S").ljust(20), str(int(x[1])).ljust(7), x[3]
)
  except MySQLdb.Error, e:
    utils.err('%d: %s' % (e.args[0], e.args[1]))
    raise DBError(ErrorCode.DB_ERROR,'%d: %s' % (e.args[0], e.args[1]))
  except MigError, me:
    utils.err('Migration Error: %s' % me.args[0])
    raise me
  finally:
    if cur:
      cur.close()
    if con:
      con.close()
