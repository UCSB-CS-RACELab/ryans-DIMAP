from ResourceTypes import *

def writeJob(ip, user, clientname, directory):
    job_name = ip + '-' + user
    opt = Options('MD5')
    inc = Include(directory, opt)
    fset= FileSet(user + '-' + ip + '-' + 'fs', inc)

    job = Job(job_name, clientname, user + '-' + ip + '-fs')
    str = fset.writeStr()
    str += job.writeStr()
    addToConf(str)
   
def addToConf(str):
    path= '/etc/bacula/bacula-dir.conf'
    with open(path, 'a') as file:
	file.write(str)    


