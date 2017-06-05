#Author: Matthew Mason	
#Description: controls wifi client connection

import subprocess
import time
import ConfigParser
from classDevice import Device
from threading import Timer


#sends system command and kill process if timer hit
def sendcmd(command):
	kill = lambda process: process.kill()
	
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	myTimer = Timer(15, kill, [p])
	try:
		myTimer.start()
		out = p.stdout.read(1000)
	finally:
		myTimer.cancel()
	return out
	

#checks if wifi client is connected to AP
def isConnected():
	checkWifi = "/sbin/ifconfig wlan0 | grep inet\ addr | wc -l"
	print "check connection"
	out = sendcmd(checkWifi)
	print out
	if '0' in out:
		return False
	elif '1' in out:
		return True
		
#connect to wifi router		
def connectWifi(Device):
	wlDown= "sudo ifconfig wlan0 down"
	wlUp = "sudo ifconfig wlan0 up"
	#remove wpa_supplicant/wlan0 file
	rmFile = "sudo rm /var/run/wpa_supplicant/wlan0"
	#command starts wpa_suplicant to enable use with wpa_cli
	startWpaSup = "sudo wpa_supplicant -B -iwlan0 -c//etc//wpa_supplicant//wpa_supplicant.conf"
	# check if wpa_supplicant is running
	wpaSupCeck = "sudo ps aux | grep wpa_suplicant"
#	sudo wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
	wpaCli ="sudo wpa_cli -p /var/run/wpa_supplicant/ "
	removeNetwork = "remove_network 0"
	scan = "scan"
	scanResults = "scan_results"
	addNetwork = "add_network"
	setSSID = "set_network 0 ssid " + '\'\"' + Device.getSSID() + '\"\''
	if Device.getPassword() == '':
		setPassword = "set_network 0 key_mgmt NONE"
	else:
		setPassword = "set_network 0 psk " + '\'\"' + Device.getPassword() + '\"\''
	enableNetwork = "select_network 0"
	requestIP = "dhclient wlan0"
	
	cmdArray = [wlDown, wlUp, startWpaSup, wpaCli + removeNetwork, wpaCli + scan, wpaCli + scanResults, wpaCli + addNetwork, 
		wpaCli + setSSID, wpaCli + setPassword, wpaCli + enableNetwork, requestIP]
	
	for cmd in cmdArray:
		if cmd == startWpaSup and "wpa_supplicant" not in sendcmd(wpaSupCeck):
			sendcmd(startWpaSup)
		elif not cmd == startWpaSup:
			print cmd
			time.sleep(1)
			out = sendcmd(cmd)
			print out
		
	return isConnected()

#get parameters from config file
def getParameters(file, section):
	device = {}
	config=ConfigParser.ConfigParser()
	config.read(file)
	options = config.options(section)
	for option in options:
		try:
			device[option] = config.get(section, option)
			if device[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			device[option] = None
	return device

#initalize device class
def initDevice(devConfig):
	device = Device(devConfig['name'], devConfig['measure'], devConfig['ssid'], devConfig['password'], devConfig['macaddr'])
	return device	

	
def main():
	print "start program"
	
	configFile = 'device.cfg'
	lastModified = ""
	checkModDate = "stat device.cfg | grep Modify"
	myPiConfig = getParameters(configFile, 'DEVICE')
	myPi = Device(configFile, 'DEVICE')

	lastModified = checkModDate
	print "my device " + myPi.getName()
	
	while True:
		time.sleep(10)

		if not isConnected():
			connectWifi(myPi)
	
