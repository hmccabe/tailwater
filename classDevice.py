class Device:

	def __init__(self, name='', measureInterval='', ssid='', password='', macAddr=''):
		self.__name = name
		self.__measureInterval=measureInterval
		self.__ssid=ssid
		self.__password = password
		self.__macAddr=macAddr
		
	def setName(self, name=''):
		self.__name = name
		
	def queryInterval(self, measureInterval=''):
		self.__measureInterval = measureInterval
	
	def setSSID(self, ssid=''):
		self.__ssid = ssid
		
	def setPassword(self, password=''):
		self.__password = password
		
	def setMacAddr(self, macAddr=''):
		self.__macAddr = macAddr
	
	def getName(self):
		name = self.__name
		return name
	def getAddr(self):
		interval = self.measureInterval
		return interval
	def getSSID(self):
		ssid = self.__ssid
		return ssid
	def getPassword(self):
		password = self.__password
		return password
	def getMacAddr(self):
		mac = self.__macAddr
		return mac

	#def getMacAddr(self):
	#	enableWlan = "sudo ifconfig wlan0 up"
	#	p = subprocess.Popen(cmdping, shell=True, stderr=subprocess.PIPE)
	#	mac, err = p.communicate()
	#	return mac
			