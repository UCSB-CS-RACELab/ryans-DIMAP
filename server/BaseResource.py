
class BaculaResource:
    
    def defaults(self):
	return {}

    def writeStr(self):
	
	name = self.resourceType()
	output = name + ' {\n'
	
	# loop through dictionary, writing keys and values.
	for k, v in self.defaults().iteritems():
	    if k in self.dictionary:
		v = self.dictionary[k]
	    output += '  ' + k + ' = ' + v + '\n'
    
	for k, v in self.subResources.iteritems():
	    output += '  ' + v.writeStr() + '\n'
     
	output += '}\n'
	return output
       
        # Must overide to set resource type
    def resourceType(self):
	return 'AbstractBaculaResource'
    
    def __init__(self):
	self.dictionary = {}
	self.subResources = {}

