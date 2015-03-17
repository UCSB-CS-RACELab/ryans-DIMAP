from BaseResource import BaculaResource

class Client(BaculaResource):
    
    def __init__(self, ip=None, password=None):
	#super(Client, self).__init__()
	self.dictionary = {}
	self.subResources = {}
	self.dictionary['Name'] = ip + '-fd' 
	self.dictionary['Address'] = ip
	self.dictionary['Password'] = password
	
    def resourceType(self):
	return 'Client'

    def defaults(self):
	return {'FDPort' : '9102',
		'Catalog' : 'MyCatalog',
		'File Retention' : '30 days',
		'Job Retention' : '6 months',
		'AutoPrune' : 'yes'}
    
    #def __init__(self):
#	self.dict = {}
     
