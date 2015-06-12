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
    
class FileSet(BaculaResource):
    
    def __init__(self, name, include):
	self.dictionary = {}
	self.subResources = {}
	self.dictionary['Name'] = name
	self.subResources['Include'] = include

    def resourceType(self):
	return 'FileSet'

class Include(BaculaResource):
    
    def __init__(self, file, options):
	self.dictionary = {}	
	self.subResources = {}
	self.dictionary['File'] = file
	self.subResources['Options'] = options
    
    def resourceType(self):
	return 'Include'

class Options(BaculaResource):
    
    def __init__(self, signature):
	self.dictionary = {}
	self.subResources = {}
	self.dictionary['signature'] = signature

    def resourceType(self):
	return 'Options'

class Job(BaculaResource):
    
    def __init__(self, name, client, fileSet):
	self.dictionary = {}
	self.subResources = {}
	self.dictionary['Name'] = name
	self.dictionary['Client'] = client
	self.dictionary['FileSet'] = fileSet

    def resourceType(self):
	return 'Job'
    
    def defaults(self):
	return {'Type' : 'Backup',
		'Level' : 'Full',
		'Schedule' : 'WeeklyCycle',
		'Storage' : 'File',
		'Messages' : 'Standard',
		'Pool' : 'File',
		'Priority' : '10',
		'Write Bootstrap' : '"/var/spool/bacula/%c.bsr"'}