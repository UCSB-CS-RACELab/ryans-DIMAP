import MySQLdb as mdb
import sys

DB_IP  = 'localhost'
DB_USER= 'BackupSys'
DB_PSW = 'mysql142'
DB     = 'BackupSys'

from ResourceTypes import *

def startBackups(user, ip):
    print "Registering for backups"
    client = ip + '-fd'
    jobname = 'backup-' + ip
    fileset = FileSet(jobname + 'fs', Include('/home/ec2-user', Options('MD5')))

    job = Job(jobname, client, jobname + 'fs')
    job.dictionary['RunAfterJob'] = '"/bacula-scripts/post-backup.py %i ' + user.replace(" ", "") + '"'

    fs = fileset.writeStr()
    job= job.writeStr()
    with open('/etc/bacula/bacula-dir.conf', 'a') as file:
	file.write(fs)
	file.write(job)




def regUsr(username, password):
    print 'Registering user' + username
    q = 'INSERT INTO Users (user_id, password) VALUES ("' + username + '", "' + password + '");'
    print q
    result = query(q)
    return result


def authJobAccess(user, jobid):
    allow = False

    q= 'SELECT J.JobID FROM JobIDs J WHERE J.User ="' + user.replace(" ", "")  + '" AND J.JobID ="'  + jobid + '";'

    print q
    result = query(q)
    if (len(result) > 0):
        print len(result)
        print result[0]
        allow = True
    return allow

def listRestoreOptions(user):

    print user.replace(" ", "")
    q = 'SELECT J.JobIDs FROM JobIDs J WHERE J.User="' + user.replace(" ", "")  + '" ;'
    q = 'SELECT * FROM JobIDs;'
    r = []
    rows = query(q)
    print rows
    #if (not rows): return 'No options found.'
    for row in rows:
        r.append(row[0])

    return r


def createJob(user, auth, IP, fdname, dir):
    r = ''

    # attempt to create the job.
    q = 'INSERT INTO BackupJobs (IP, User, Directory, FdName, SysTag) VALUES ("' + IP + \
	'", "' + user + '", "' + dir + '", "' + fdname + '", "W");'
    return query(q)

def listJobs(user):
    r = []

    # List the user's jobs.
    q = 'SELECT J.IP, J.Directory FROM BackupJobs J WHERE J.User="'+user+'";'
    print q
    rows = query(q)
    print rows
    if (not rows): return 'No jobs found.'
    for row in rows:
	r.append([row[0], row[1]])

    return r

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




def query(q):
    try:
        print "Accessing the database."
    	con = mdb.connect(DB_IP, DB_USER, DB_PSW, DB)
    	cur = con.cursor()

    	cur.execute(q)
    	con.commit()
    	rows = cur.fetchall()

        print rows

        if (con):
            con.close()

        return rows

    except mdb.Error, error:
        print error
    	print "Error reading from the MYSQL database."
    	sys.exit(1)

    return None


def listUsers():
    r = ''
    q = 'SELECT user_id FROM Users;'
    return query(q)
