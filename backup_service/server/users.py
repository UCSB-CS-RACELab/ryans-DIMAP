import MySQLdb as mdb

DB_IP  = 'localhost'
DB_USER= 'BackupSys'
DB_PSW = 'mysql142'
DB     = 'BackupSys'

from ResourceTypes import *

def start_backups(user, ip):
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
 
def auth_usr(user, auth):
    allow = False
    return True; # TODO: Fix 
    q= 'SELECT U.auth FROM Users U WHERE U.name ="' + user + '" AND U.auth ="'  + auth + '";'
    print q
    result = query(q)
    if (len(result) > 0):
	print len(result)
	print result[0]
	allow = True
    return allow


def reg_usr(user):
    print 'Registering user' + user
    q = 'INSERT INTO Users (user_id) VALUES ("' + user + '");'
    print q
    result = query(q)
    return result


def auth_job_access(user, jobid):
    allow = False

    q= 'SELECT J.JobId FROM JobIDs J WHERE J.User ="' + user.replace(" ", "")  + '" AND J.JobID ="'  + jobid + '";'
    print q
    result = query(q)
    if (len(result) > 0):
        print len(result)
        print result[0]
        allow = True
    return allow

#TODO: Make method authorize user.
def list_restore_options(user, auth):
    # authorize the user. 
    #if (not auth_usr(user, auth)):
	#return 'List Restore Options: Permission Denied, Authentication Failure.'
    print user.replace(" ", "") 
    q = 'SELECT J.JobID FROM JobIDs J WHERE J.User="' + user.replace(" ", "")  + '" ;'
    r = [] 
    rows = query(q)
    print rows
    if (not rows): return 'List Restore Options: Failed to list options.'
    for row in rows:
	r.append(row[0])
    
    return r
    

     

def create_job(user, auth, IP, fdname, dir):
    r = ''
    # authorize the user. 
    if (not auth_usr(user, auth)):
	return 'Create Job: Permission Denied, Authentication Failure.'
    
    # attempt to create the job.
    q = 'INSERT INTO BackupJobs (IP, User, Directory, FdName, SysTag) VALUES ("' + IP + \
	'", "' + user + '", "' + dir + '", "' + fdname + '", "W");'
    return query(q)
    
def list_jobs(user, auth):
    r = []
    #authorize the user.
    if (not auth_usr(user, auth)):
	return 'List Jobs: Permission Denied, Authentication Failure.'
    
    # List the user's jobs.
    q = 'SELECT J.IP, J.Directory FROM BackupJobs J WHERE J.User="'+user+'";'
    print q
    rows = query(q)
    print rows
    if (not rows): return 'List Jobs: Failed to list jobs.'
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
    r = ''
    try:
	con = mdb.connect(DB_IP, DB_USER, DB_PSW, DB)
	cur = con.cursor()

	cur.execute(q)
	con.commit()
	rows = cur.fetchall()
	
	r = rows    

	#for row in rows:
	#    r += str(row)


    except _mysql.Error, error:

	print "Error %d: %s" % (error.args[0], error.args[1])
	sys.exit(1)

    finally:

	if con:
	    con.close()
	return r



def list_users():
    r = ''
    q = 'SELECT user_id FROM Users;'
    return query(q)