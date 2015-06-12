
from twisted.web.resource import Resource
import json
import jwt
import tasks

class Service(Resource):
	isLeaf = True


	def render_GET(self, request):
		print request.getAllHeaders()
		content = {"available commands": ["start-backups", "list-jobs"]};
		return json.dumps(content);

	def render_POST(self, request):
		jwtUser = self.getUser(request.getHeader('x-jwt-assertion'))
		print "User as passed by the gateway: " + jwtUser
		postData = request.content.read()
		print str(postData)

		receivedJSON = json.loads(postData)

		command = receivedJSON['command'];
		user = receivedJSON['user'];
		if ((user + '@carbon.super') != jwtUser):
			print 'Provided user name does not match authenticated user name.'
			return 'Provided user name does not match authenticated user name.'


		if (command == 'start-backups'):
			return self.startBackups(receivedJSON)
		elif (command == 'list-jobs'):
			return self.listJobs(receivedJSON)
		elif (command == 'add-user'):
			return 'Please add users through the WSO2 gateway.'
		elif (command == 'auth-test'):
			return 'Authentication Successful'
		elif (command == 'restore-new-machine'):
			return self.restoreNewMachine(receivedJSON)
		elif (command == 'list-available'):
			return self.listAvailable(receivedJSON)


		else: return "Invalid command"


	def getUser(self, jwtString):
		return jwt.decode(jwtString, verify=False)['http://wso2.org/claims/enduser']

		# Backup operations

	def startBackups(self, receivedJSON):
		userName = receivedJSON['user']
		ipAddress = receivedJSON['ip']
		tasks.startBackups(userName, ipAddress)
		from subprocess import call
		status = call("./scripts/setup-backups.sh -m " + ipAddress, shell=True)
		print "Status: " + str(status)
		return "Status: " + str(status)


	def listJobs(self, receivedJSON):
		userName = receivedJSON['user']
		return tasks.listJobs(userName)

	def listAvailable(self, receivedJSON):
		userName = receivedJSON['user']
		return str(tasks.listRestoreOptions(userName))

# Restore operations

	def restoreNewMachine(self, receivedJSON):
		userName = receivedJSON['user']
		ipAddress = receivedJSON['ip']
		restoreOption = receivedJSON['restoreOption']

		authorizedUser = tasks.authJobAccess(userName, restoreOption)
		if (not authorizedUser):
			return "You do not have permission to access this backup."

		from subprocess import call
		status = call("./scripts/restore-new-machine.sh -j " + restoreOption + " -m " + ipAddress, shell=True)
		print "Status: " + str(status)
		return "Status: " + str(status)


# User operations

	def addUser(receivedJSON):
		userName = receivedJSON['user']
		print 'User \'' + userName + '\' should get created at this point.'
		return tasks.reg_usr(userName, password)
