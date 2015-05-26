from twisted.web.resource import Resource
import json

class StatusService(Resource):
	isLeaf = True
	def render_GET(self, request):
		content = {"Status": "Available"};
		return json.dumps(content);
		