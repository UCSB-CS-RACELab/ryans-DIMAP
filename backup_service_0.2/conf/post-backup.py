#!/usr/bin/python

# Post backup script that bacula should run after a job so that the job gets associated with the correct user.

import MySQLdb as mdb
import sys

DB_IP  = 'localhost'
DB_USER= 'BackupSys'
DB_PSW = 'mysql142'
DB     = 'BackupSys'

USER=sys.argv[2]
JOB=sys.argv[1]

print USER
print JOB

def insert(q):
    r = ''
    try:
        con = mdb.connect(DB_IP, DB_USER, DB_PSW, DB)
        cur = con.cursor()

        cur.execute(q)
        #rows = cur.fetchall()
        #r = rows    

    except _mysql.Error, error:

        print "Error %d: %s" % (error.args[0], error.args[1])
        sys.exit(1)

    finally:

        if con:
            print 'hi'
            #con.close()
        return r

q='INSERT INTO JobIDs (JobID, User) VALUES ("' + JOB + '", "' + USER + '");'
insert(q)
