
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import sys
import logging
import time
import json
import getopt
from classDevice import Device

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

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("property: " + str(payloadDict["state"]["desired"]["property"]))
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")
		
def customShadowCallback_Delta(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	print(responseStatus)
	payloadDict = json.loads(payload)
	print("++++++++DELTA++++++++++")
	print("property: " + str(payloadDict["state"]["property"]))
	print("version: " + str(payloadDict["version"]))
	print("+++++++++++++++++++++++\n\n")

def customShadowCallback_Delete(payload, responseStatus, token):
	if responseStatus == "timeout":
		print("Delete request " + token + " time out!")
	if responseStatus == "accepted":
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Delete request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Delete request " + token + " rejected!")

#state is either desired or reported, property is the actual parameter to change, value the value to which the parmeter is to be set 
def shadowUpdater(state, property, value):

	#get info from config file
	configFile = 'device.cfg'
	configSection = 'DEVICE'
	myPi = Device(configFile, configSection)
	host = myPi.getEndpoint()
	rootCAPath = myPi.getRootCA()
	certificatePath = myPi.getCertPem()
	privateKeyPath = myPi.getPrivateKey()
	thingID = myPi.getName()

	# Configure logging
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)

	# Init AWSIoTMQTTShadowClient
	myAWSIoTMQTTShadowClient = None


	myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(thingID)
	myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	#AWSIoTMQTTShadowClient configuration
	myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
	myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

	# Connect to AWS IoT
	#myAWSIoTMQTTShadowClient.connect()

	# Create a deviceShadow with persistent subscription
	#Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingID, True)

	#while True:
	JSONPayload = '{"state":{ "' + state + '":{"' + property + '": "' + str(value) + '"}}}'

	myMQTTClient = myAWSIoTMQTTShadowClient.getMQTTConnection()
	myMQTTClient.publish("$aws/things/" +thingID+"/shadow/update",JSONPayload,1)
	#Bot.shadowRegisterDeltaCallback(customShadowCallback_Delta)
	#Bot.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)

