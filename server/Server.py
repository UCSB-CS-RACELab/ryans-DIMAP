from twisted.web import xmlrpc, server
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
import Users

class Example(xmlrpc.XMLRPC):
    """
    An example object to be published.
    """

    def xmlrpc_echo(self, x):
        """
        Return all passed args.
        """
        return x

    def xmlrpc_users(self):
	"""
	Return a list of users.
	"""
	return Users.list_users()    

    def xmlrpc_create_backup(self, user, auth, IP, fd, dir):
	"""
	Create a backup job description for the user.
	"""
	return Users.create_job(user, auth, IP, fd, dir)

    def xmlrpc_list_jobs(self, user, auth):
	"""
	List the user's jobs.
	"""
	return Users.list_jobs(user, auth)

    def xmlrpc_list_restore_options(self, user, auth):
	"""
	List the jobs the user can use for a restore
	"""
	return Users.list_restore_options(user, auth)

    def xmlrpc_restore_new_machine(self, user, auth, IP, jobid):
	"""
	Restore a new machine from selected job id
	"""
	if not Users.auth_job_access(user, jobid):
	    return 'Permission Denied, you do not have access to this job.'
    
	from subprocess import call
	status = call("./restore-new-machine.sh -m " + IP + " -j " + jobid, shell=True)
	print status
	return 'Done'

    def xmlrpc_fault(self):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        raise xmlrpc.Fault(123, "The fault procedure is faulty.")

class PageServer(Resource):
    def render_GET(self, request):
        return "The Server is Operational!"

if __name__ == '__main__':
    from twisted.internet import reactor
    r =  Example()
    
    reactor.listenTCP(9080, server.Site(r))
    reactor.run()

