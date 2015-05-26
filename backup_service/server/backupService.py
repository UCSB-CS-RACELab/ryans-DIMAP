
from twisted.web.resource import Resource
import json
import users

class BackupService(Resource):
	isLeaf = True
	def render_GET(self, request):
		content = {"available commands": ["start-backups", "list-jobs"]};
		return json.dumps(content);

	def render_POST(self, request):
		postData = request.content.getvalue()
		postJSON = json.loads(postData)
		print postJSON['command']
		self.handleCommand(postJSON['command'])
		return ""

	def handleCommand(self, command):
		if (command['name'] == 'start-backups'):
			userName = command['user']
			ipAddress = command['ip']
			print 'Backups should be started at this point.'
			users.start_backups(userName, ipAddress)
			from subprocess import call
			status = call("./scripts/setup-backups.sh -m " + ipAddress, shell=True)
			print status

			return 'Done' 
		#Users.reg_usr(user_id)
		elif (command['name'] == 'list-jobs'):
			userName = command['user']
			print 'Jobs should be listed now.'
