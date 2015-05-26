from twisted.web.resource import Resource
import json
import users

class AdminService(Resource):
	isLeaf = True
	def render_GET(self, request):
		content = {"available commands": ["list-users"]};
		return json.dumps(content);

	def render_POST(self, request):
		postData = request.content.getvalue()
		postJSON = json.loads(postData)
		print postJSON['command']
		self.handleCommand(postJSON['command'])
		return ""

	def handleCommand(self, command):
		if (command['name'] == 'list-users'):
			print 'A list of users should be returned at this point.'
			print users.list_users()


		