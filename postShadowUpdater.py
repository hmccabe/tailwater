
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


#state is either desired or reported, property is the actual parameter to change, value the value to which the parmeter is to be set 
def shadowUpdater(state, property, value):
	JSONPayload = '{\"' + property + '\": \"' + str(value) + '\"}'
	req = urllib2.Request( 'https://ihh4jaogw9.execute-api.us-west-2.amazonaws.com/UpdateShadowV1/updateshadow')
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, JSONPayload)
	print response
