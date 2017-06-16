# Tailwater Systems ORP Probe Readers #
This project uses Raspberry Pi 3 to take readings from ORP probes, perform heuristics, and sync the data with the cloud.

## Raspberry Pi ## 
### ORP Probe Polling Scripts ###
orp_manager.py (main script)
ORPI2C.py
AWSIoTClient.py
### Local Interface ###
initialSetup.py
### tmeplates ###
advance.html
form.html
### Config file ###
classDevice.py
device.cfg
### wireless control ###
runWifiClient.py
wifiSetup.py
### ThingShadow control ###
basicShadowDelta Listener
postShadowUpdater

## AWS ##
- The files in the lambda directory are copies of the AWS Lambda functions.
- The files in the www directory are hosted on the AWS EC2 web server.
