from twisted.web.resource import Resource
import json
import users

class RestoreService(Resource):
	isLeaf = True
	def render_GET(self, request):
		content = {"available commands": ["restore-new-machine", "list-available"]};
		return json.dumps(content);

	def render_POST(self, request):
		postData = request.content.getvalue()
		postJSON = json.loads(postData)
		print postJSON['command']
		return self.handleCommand(postJSON['command'])
		

	def handleCommand(self, command):
		if (command['name'] == 'restore-new-machine'):
			userName = command['user']
			ipAddress = command['ip']
			jobid = command['jobid']
			print 'A new machine should be restored at this point.'
    
			from subprocess import call
			status = call("./scripts/restore-new-machine.sh -m " + ipAddress + " -j " + jobid, shell=True)
			print status
			return 'Done'
		elif (command['name'] == 'list-available'):
			userName = command['user']
			print 'Available restores should be listed now.'
			jsonResult = json.dumps(users.list_restore_options(userName, "")) #'{"backups":"' + + '"}'
			print jsonResult
			return jsonResult
