
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

import json
import urllib2

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


#uses post request to trigger aws lambda fuction and update thing shadow. 
def shadowUpdater(state, property, value):
	#formatted string for JSON request
	JSONPayload = '{\"' + property + '\": \"' + str(value) + '\"}'
	#lambda url
	req = urllib2.Request( 'https://ihh4jaogw9.execute-api.us-west-2.amazonaws.com/UpdateShadowV1/updateshadow')
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, JSONPayload)

