#checks if specified python script is running and starts it if not.
from classDevice import Device
import subprocess
import time

#Initialize Device
configFile = 'device.cfg'
configSection = 'DEVICE'
myPi = Device(configFile, configSection)

def sendcmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read(500)
	return out

if __name__ == '__main__':
	while True:
		time.sleep(10)
		try:	
			sendcmd('sudo route del default gw 192.168.50.1 metric 0')
			sendcmd('sudo route add default gw 192.168.50.1 metric 405')
			programArray  = ['runWiFiClient', 'initialSetup', 'basicShadowDeltaListener', 'orp_manager']
			grepProgram = "ps ax | grep "
			startScript = 'sudo python2.7 ./'
			dotpy = '.py > /dev/null 2>&1 &'
			if not startScript + programArray[0] in sendcmd(grepProgram + programArray[0]):
				if not myPi.getSSID() == '':
					sendcmd(startScript + programArray[0] + dotpy)
		
			if not startScript + programArray[1] in sendcmd(grepProgram + programArray[1]):
				sendcmd(startScript + programArray[1] + dotpy)
			
			if not startScript + programArray[2] in sendcmd(grepProgram + programArray[2]):
				sendcmd(startScript + programArray[2] + dotpy)	

			while not startScript + programArray[3] in sendcmd(grepProgram + programArray[3]):
				if not myPi.getRootCA() == '' or not myPi.getCertPem() == '' or not myPi.getPrivateKey() == '':
					sendcmd(startScript + programArray[3] + dotpy)

		except Exception as e:
			print e
			pass
	
