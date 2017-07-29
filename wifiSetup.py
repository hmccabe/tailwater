#Author: Matthew Mason	
#Description: controls wifi client connection

import subprocess
import time
from classDevice import Device
from threading import Timer
import ORPI2C
from postShadowUpdater import updatePollInterval, updateORPVal


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
	out = sendcmd(checkWifi)
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
	uapDown= "sudo ifconfig uap0 down"
	uapUp = "sudo ifconfig uap0 up"

	setSSID = "set_network 0 ssid " + '\'\"' + Device.getSSID() + '\"\''
	if Device.getPassword() == '':
		setPassword = "set_network 0 key_mgmt NONE"
	else:
		setPassword = "set_network 0 psk " + '\'\"' + Device.getPassword() + '\"\''
	enableNetwork = "select_network 0"
	requestIP = "dhclient wlan0"
	
	cmdArray = [wlDown, wlUp, startWpaSup, wpaCli + removeNetwork, wpaCli + scan, wpaCli + scanResults, wpaCli + addNetwork, 
		wpaCli + setSSID, wpaCli + setPassword, uapDown, wpaCli + enableNetwork, requestIP, uapUp]
	
	for cmd in cmdArray:
		if cmd == startWpaSup and "wpa_supplicant" not in sendcmd(wpaSupCeck):
			sendcmd(startWpaSup)
		else:
			time.sleep(1)
			#if ssid not found abort process and start over on next loop
			if scanResults in cmd:
				out = sendcmd(cmd)
				print out
				if not Device.getSSID() in out:
					return isConnected()
			else:
				
				out = sendcmd(cmd)
				print out
	return isConnected()


def main():
	
	configFile = 'device.cfg'
	lastModified = ""
	checkModDate = "stat device.cfg | grep Modify"
	myPi = Device(configFile, 'DEVICE')

	lastModified = checkModDate
	
	while True:
		time.sleep(10)

		if not isConnected():
			if connectWifi(myPi):
				time.sleep(30)
				#get wlan0 ipaddr and reset route table setting wlan0 as default
				output = sendcmd('sudo route -n | grep wlan0')
                        	wordList = output.split()
                        	ipaddr = wordList[1]
				sendcmd('sudo route add default dev wlan0 gw ' + ipaddr + ' metric 0')
				time.sleep(30)
				sensor = ORPI2C.Probe()
				reading = sensor.poll()
				#update hwclock on wificonnection
				sendcmd('sudo /etc/init.d/ntp stop')
				sendcmd('sudo ntpd -q -g')
				sendcmd('sudo /etc/init.d/ntp start')
				sendcmd('sudo hwclock -w')
				sendcmd('sudo hwclock -s') 
				updatePollInterval(myPi.getName(), "pollInterval", myPi.getPollInterval())
				updateORPVal(myPi.getName(), "orpval", str(reading))
	
