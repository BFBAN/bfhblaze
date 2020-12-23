#!/usr/bin/env python2.5

from utils import *
import unittest

class TestUtils(unittest.TestCase):
    def testHandleMessage(self):
        handle_msg('TEST','TEST')

    def testHandleMessageNone(self):
        handle_msg(None,None)

    def testGetcon(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'

        try:
            conn = get_con(opts)
            self.failIf(conn is None,'Could not establish a connection')
            conn.close()
        except DatabaseConfigurationError,de:
            self.fail('Failed to initialize database connection')

    def testGetconBadConfNone(self):
        opts = None
        self.assertRaises(DatabaseConfigurationError,get_con,opts)

    def testGetconBadConfInvalid(self):
        opts = 'port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        self.assertRaises(DatabaseConfigurationError,get_con,opts)

    def testGetconFail(self):
        opts = 'host=elephant.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        self.assertRaises(DatabaseConfigurationError,get_con,opts)

    def testParseDbOpts(self):
        opts = 'host=elephant.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        options = parse_dbopts(opts)
        self.failIf(not options.has_key('host'), 'Missing host key')
        self.failIf(not options.has_key('port'), 'Missing port key')
        self.failIf(not options.has_key('user'), 'Missing user key')
        self.failIf(not options.has_key('passwd'), 'Missing passwd key')
        self.failIf(not options.has_key('db'), 'Missing db key')

    def testParseDbOptsNoPort(self):
        opts = 'host=elephant.online.ea.com,user=dbmig,passwd=dbmig,db=dbmig_test'
        options = parse_dbopts(opts)
        self.failIf(not options.has_key('port'), 'Missing default port key')

    def testParseDbOptsInvalid(self):
        opts = 'hostelephant.online.ea.com,user=dbmig,passwd=dbmig,db=dbmig_test'
        self.assertRaises(DatabaseConfigurationError,parse_dbopts,opts)

    def testGetScriptName(self):
        sname = get_script_name(1,'league')
        self.assertEqual(sname,'001_league.sql')

    def testGetScriptNameNone(self):
        self.assertRaises(ParamError,get_script_name,None,None)

    def testGetMigrationPath(self):
        component = 'league'
        cpath = 'component/league/'
        version = 1
        p = get_migration_path(component, cpath, version)
        self.assertEqual(p,'component/league/001_league.sql')
    
    def testGetMigrationPathNone(self):
        self.assertRaises(ParamError,get_migration_path,None,None,None)

    def testFindMigration(self):
        component = 'test'
        cpath = './component/test/db/mysql/'
        version = 1
        p = find_migration(component,cpath,version)
        self.assertEqual(p,cpath+'001_test.sql')

    def testFindMigrationNone(self):
        self.assertRaises(ParamError,find_migration,None,None,None)
    
    def testLoadSQL(self):
        component = 'test'
        cpath = './component/test/db/mysql/'
        version = 1
        p = find_migration(component,cpath,version)
        sql = load_sql(p)
        self.failUnless(sql,'SQL statements missing.')

    def testLoadSQLNone(self):
        p = './component/test/db/mysql/00N_test.sql'
        sql = load_sql(p)
        self.assertEqual(sql,None,'SQL  missing not detected properly.')

    def testCheckVersionTable(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            self.assertRaises(MySQLdb.Error,cur.execute,'select * from blaze_schema_info')
            check_version_table(cur,'../../')
            try:
                cur.execute('select * from blaze_schema_info')
            except MySQLdb.Error, me:
                fail('Schema not properly created.')
            cur.execute('drop table blaze_schema_info')
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def testCheckVersionTableInvalid(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            self.assertRaises(DatabaseConfigurationError,check_version_table,cur,'../')
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def testGetCurrentVersion(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            check_version_table(cur,'../../')
            cur.execute('insert into blaze_schema_info (component,version,last_updated,fingerprint,notes) values (\'test\',\'2\',now(),\' \',\' \')')
            val = get_current_version(cur,'test')
            self.assertNotEqual(val,None)
            self.assertEqual(len(val),2)
            self.assertEqual(val[0],2)
        finally:
            cur.execute('drop table blaze_schema_info')
            if cur:
                cur.close()
            if con:
                con.close()

    def testGetCurrentVersionNone(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            self.assertRaises(ParamError,get_current_version,cur,None)
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def testGenerateFingerprint(self):
        sql = 'DROP TABLE BLAZE_SCHEMA_INFO'
        fp1 = generate_fingerprint(sql)
        fp2 = generate_fingerprint('DROP TABLE BLAZE_SCHEMA_INFO')
        self.assertEqual(fp1,fp2)
        fp3 = generate_fingerprint('SHOW TABLES')
        self.assertNotEqual(fp1,fp3)

    def testSetVersion(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            check_version_table(cur,'../../')
            set_version(cur,'test',2,' ')
            val = get_current_version(cur,'test')
            self.assertNotEqual(val,None)
            self.assertEqual(len(val),2)
            self.assertEqual(val[0],2)
            set_version(cur,'test',3,' ')
            val = get_current_version(cur,'test')
            self.assertNotEqual(val,None)
            self.assertEqual(len(val),2)
            self.assertEqual(val[0],3)
            set_version(cur,'test',0,' ')
            val = get_current_version(cur,'test')
            self.assertNotEqual(val,None)
            self.assertEqual(len(val),2)
            self.assertEqual(val[0],-1)
        finally:
            cur.execute('drop table blaze_schema_info')
            if cur:
                cur.close()
            if con:
                con.close()

    def testSetVersionNone(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            self.assertRaises(ParamError,set_version,cur,None,None,None)
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def testGetTableNames(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            cur.execute('CREATE TABLE A (col1 int(10))')
            cur.execute('CREATE TABLE C (col1 int(10))')
            cur.execute('CREATE TABLE B (col1 int(10))')
            t = get_table_names(cur,'dbmig_test')
            self.assertEqual(len(t),3)
        finally:
            cur.execute('DROP TABLE A')
            cur.execute('DROP TABLE C')
            cur.execute('DROP TABLE B')
            if cur:
                cur.close()
            if con:
                con.close()

    def testGetTableSQL(self):
        opts = 'host=tiger.online.ea.com,port=3306,user=dbmig,passwd=dbmig,db=dbmig_test'
        try:
            con = get_con(opts)
            cur = con.cursor()
            cur.execute('CREATE TABLE TEST (col1 int(10))')
            sql = get_table_sql(cur,'TEST')
            self.assertNotEqual(sql,None)
        finally:
            cur.execute('DROP TABLE TEST')
            if cur:
                cur.close()
            if con:
                con.close()

if __name__ == '__main__':
    unittest.main()
