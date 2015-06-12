from suds.client import Client
from suds.transport.http import HttpAuthenticated
import logging

if __name__ == '__main__':

	#logging.basicConfig(level=logging.INFO)
    #logging.getLogger('suds.client').setLevel(logging.DEBUG)

	if len(sys.argv) < 3:
		print "Usage " + sys.argv[0] + " <username> <password>"
		return

	username = sys.argv[1];
	password = sys.argv[2];
    
    t = HttpAuthenticated(username='admin', password='admin')
    client = Client('https://128.111.179.151:9443/services/UserAdmin?wsdl', location='https://128.111.179.151:9443/services/UserAdmin', transport=t)
    #print client#.service.listAllUsers()
    print client.service.addUser(username, password, ['Internal/subscriber'], [], username )