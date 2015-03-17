import MySQLdb as mdb

DB_IP  = 'localhost'
DB_USER= 'BackupSys'
DB_PSW = 'PWD'
DB     = 'BackupSys'

def auth_usr(user, auth):
    allow = False
    
    q= 'SELECT U.auth FROM Users U WHERE U.name ="' + user + '" AND U.auth ="'  + auth + '";'
    print q
    result = query(q)
    if (len(result) > 0):
	print len(result)
	print result[0]
	allow = True
    return allow

def auth_job_access(user, jobid):
    allow = False

    q= 'SELECT J.JobId FROM JobIDs J WHERE J.User ="' + user + '" AND J.JobID ="'  + jobid + '";'
    print q
    result = query(q)
    if (len(result) > 0):
        print len(result)
        print result[0]
        allow = True
    return allow

def list_restore_options(user, auth):
    # authorize the user. 
    if (not auth_usr(user, auth)):
	return 'List Restore Options: Permission Denied, Authentication Failure.'
    
    q = 'SELECT J.JobID FROM JobIDs J, Users U WHERE U.name=J.User AND U.name="' + user + '" ;'
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
    

def query(q):
    r = ''
    try:
	con = mdb.connect(DB_IP, DB_USER, DB_PSW, DB)
	cur = con.cursor()

	cur.execute(q)

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
    q = 'SELECT name FROM Users;'
    return query(q)

