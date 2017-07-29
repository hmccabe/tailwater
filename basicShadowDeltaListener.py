'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import sys
import logging
import time
import json
import getopt
from classDevice import Device
from wifiSetup import isConnected
from basicShadowUpdater import shadowUpdater
import ast
import ORPI2C
import sys
import os

# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>
#		}
#	}
#}
#get info from config file
configFile = 'device.cfg'
configSection = 'DEVICE'
myPi = Device(configFile, configSection)

def restart_program():
	"""Restarts the current program.
	Note: this function does not return. Any cleanup action (like
	saving data) must be done before calling this function."""
 	python = sys.executable
	os.execl(python, python, * sys.argv)

def customShadowResponse(payload, responseStatus, token):
	if 'delta' in responseStatus:
		payloadDict = ast.literal_eval(json.dumps(json.loads(payload)))

		for dict in payloadDict:
			for k, v in payloadDict.iteritems():
				if k == 'state':
					for k1, v1 in v.iteritems():
						JSONPayload = '{"state":{"reported":{"' + k1 + '": "' + str(v1) + '"}}}'
						if k1 == 'pollInterval':
							Bot.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
							myPi.setPollInterval(v1)
						if k1 == 'orpval':
							sensor = ORPI2C.Probe()
							reading = sensor.poll() 
							JSONPayload = '{"state":{"reported":{"' + k1 + '": "' + str(reading) + '"}, "desired":{"' + k1 + '": "' + str(reading) + '"}}}'
							Bot.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
					return
	
def customShadowCallback_Update(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("property: " + str(payloadDict["state"]["reported"]))
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")
	
#if isConnected():

useWebsocket = False
host = myPi.getEndpoint()
rootCAPath = myPi.getRootCA()
certificatePath = myPi.getCertPem()
privateKeyPath = myPi.getPrivateKey()
thingID = myPi.getName()


try:
	if not rootCAPath == "" and not certificatePath == "" and not privateKeyPath == "" and not thingID == "":
		# Configure logging
		logger = logging.getLogger("AWSIoTPythonSDK.core")
		logger.setLevel(logging.DEBUG)
		streamHandler = logging.StreamHandler()
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		streamHandler.setFormatter(formatter)
		logger.addHandler(streamHandler)
		# Init AWSIoTMQTTShadowClient
		myAWSIoTMQTTShadowClient = None
		if useWebsocket:
			myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowDeltaListener", useWebsocket=True)
			myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
			myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
		else:
			myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(thingID)
			myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
			myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
		# AWSIoTMQTTShadowClient configuration
		myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
		myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
		myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec	

		# Connect to AWS IoT
		myAWSIoTMQTTShadowClient.connect()

		# Create a deviceShadow with persistent subscription
		Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingID, True)

		# Listen on deltas
		Bot.shadowRegisterDeltaCallback(customShadowResponse)
except Exception as ex:
	template = "An exception of type {0} occurred. Arguments:\n{1!r}"
	message = template.format(type(ex).__name__, ex.args)
	print message
	if type(ex).__name__ == 'gaierror':
		restart_program()
# Loop forever
while True:
	pass
