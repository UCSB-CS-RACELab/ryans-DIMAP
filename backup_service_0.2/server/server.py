from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
import time
import json


from service import Service
#from restoreService import RestoreService
#from userService import UserService
#from adminService import AdminService
#from statusService import StatusService

PORT = 9080

root = Resource()

root.putChild("backup", Service())
#root.putChild("restore", RestoreService())
#root.putChild("user", UserService())
#root.putChild("admin", AdminService())
#root.putChild("status", StatusService())


factory = Site(root)

#factory = Site(Service())
reactor.listenTCP(PORT, factory)
reactor.run()
