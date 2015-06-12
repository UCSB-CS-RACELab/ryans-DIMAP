from twisted.web.resource import Resource
import json
import users

class UserService(Resource):
	isLeaf = True
	def render_GET(self, request):
		# return some information about the UserService
		content = {"available commands": ["add-user", "auth-test"]};
		return json.dumps(content);

	def render_POST(self, request):
		postData = request.content.read()
		print postData

		receivedJSON = json.loads(postData)
		command = receivedJSON['command'];

		if (command == 'add-user'):
			return self.addUser(receivedJSON)
		elif (command == 'auth-test'):
			return self.authTest(receivedJSON)
		else: return "Invalid command"



	def addUser(receivedJSON):
		userName = receivedJSON['user']
		print 'User \'' + userName + '\' should get created at this point.'
		return users.reg_usr(userName, password)

	def authTest(receivedJSON):
		userName = receivedJSON['user']
		return "User '" + userName + "' authenticated"
