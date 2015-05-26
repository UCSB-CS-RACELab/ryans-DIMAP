from twisted.web.resource import Resource
import json
import users

class UserService(Resource):
	isLeaf = True
	def render_GET(self, request):
		content = {"available commands": ["create-user"]};
		return json.dumps(content);

	def handleCommand(self, command):
		if (command['name'] == 'create-user'):
			userName = command['user']
			print 'User \'' + userName + '\' should get created at this point.'
			print users.reg_usr(userName)

	def render_POST(self, request):
		postData = request.content.getvalue()
		postJSON = json.loads(postData)
		print postJSON['command']
		self.handleCommand(postJSON['command'])
		return ""

	

		