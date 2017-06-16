#Author: Matthew Mason
#Description: classDevice interacts directly with device.cfg file to set and get parameters
import ConfigParser

class Device:

	def __init__(self, file, section):
		#config file location and desired section
		self.__file=file
		self.__section=section

	#set individual paramter in config file
	def setConfigParam(self,paramName, value):
		config = ConfigParser.ConfigParser()
		config.read(self.__file)
		config.set(self.__section, paramName, value)
		with open('device.cfg', 'wb') as configfile:
			config.write(configfile)
		
	#retrurns specified parameter 
	def getConfigParam(self,paramName):
		device = {}
		config=ConfigParser.ConfigParser()
		file = self.__file
		section = self.__section
		config.read(file)
		options = config.options(section)
		for option in options:
			try:
				device[option] = config.get(section, option)
				if device[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				devConfig[option] = None
		return device[paramName]
		
				
	def setName(self, name=''):
		self.setConfigParam('NAME', name)
		
	def setPollInterval(self, measureInterval=''):
		self.setConfigParam('MEASURE', measureInterval)
		
	
	def setSSID(self, ssid=''):
		self.setConfigParam('SSID', ssid)
		
	def setPassword(self, password=''):
		self.setConfigParam('PASSWORD', password)
		
	def setMacAddr(self, macAddr=''):
		self.setConfigParam('MACADDR', macAddr)
		
	def setEndpoint(self, endpoint=''):
		self.setConfigParam('ENDPOINT', endpoint)
		
	def setRootCA(self, rootca=''):
		self.setConfigParam('ROOTCA', rootca)
		
	def setPrivateKey(self, privatekey=''):
		self.setConfigParam('PRIVATEKEY', privatekey)
		
	def setCertPem(self, certpem=''):
		self.setConfigParam('CERTPEM', certpem)
		
	def setLowLimit(self, low=''):
		self.setConfigParam('LOWLIMIT', certpem)
		
	def setHighLimit(self, high=''):
		self.setConfigParam('HIGHLIMIT', high)
		
	def setUploadInterval(self, upload=''):
		self.setConfigParam('UPLOADINTERVAL', upload)
	
	def getName(self):
		return self.getConfigParam('name')
		
	def getPollInterval(self):
		interval = self.getConfigParam('measure')
		return interval
		
	def getSSID(self):
		ssid = self.getConfigParam('ssid')
		return ssid
		
	def getPassword(self):
		password = self.getConfigParam('password')
		return password
		
	def getMacAddr(self):
		mac  = self.getConfigParam('macaddr')
		return mac
	
	def getEndpoint(self):
		endpoint = self.getConfigParam('endpoint')
		return endpoint
	
	def getRootCA(self):
		rootca  = self.getConfigParam('rootca')
		return rootca
		
	def getPrivateKey(self):
		privatekey  = self.getConfigParam('privatekey')
		return privatekey
	
	def getCertPem(self):
		certpem  = self.getConfigParam('certpem')
		return certpem

	def getHighLimit(self):
		high = self.getConfigParam('highlimit')
		return high
		
	def getLowLimit(self):
		low  = self.getConfigParam('lowlimit')
		return low
		
	def getUploadInterval(self):
		upload  = self.getConfigParam('uploadinterval')
		return upload
