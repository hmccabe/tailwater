#Author; Matthew Mason
#Description: runs flask application to connect to Pi virtual ap in order to iniate settings for client connection and genernal operation

from flask import Flask, render_template, flash, request, jsonify
from flask.ext.uploads import UploadSet, configure_uploads, AllExcept,EXECUTABLES,ALL
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import ConfigParser
import subprocess
from wifiSetup import isConnected
import time
import ORPI2C
from classDevice import Device

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


files = UploadSet('file', ALL)
app.config['UPLOADS_DEFAULT_DEST'] = 'static'
configure_uploads(app, files)

#Initialize Device
configFile = 'device.cfg'
configSection = 'DEVICE'
uploadDirectory = 'static/file/'
myPi = Device(configFile, configSection)

class BasicSetup():
	queryInterval = TextField('Query Interval:', validators=[validators.required(), validators.Length(min=1, max=2)])
	password = TextField('Password:', validators=[validators.required()])
	ssid = TextField('Router SSID', validators=[validators.required(), validators.Length(min=1, max=35)])
	
class AdvancedSetup():
	devId = TextField('Device Id:', validators=[validators.required()])
	endpoint = TextField('Endpoint:', validators=[validators.required()])
	
def updateAdvancedConfig(devId, endpoint, rootCA, privatePem, certPem):
	#device.cfg location
	configFile = 'device.cfg'
	configSection = 'DEVICE'

#get wifi client mac
def getMacAddr():
	getMac = "ifconfig wlan0 | grep HWaddr"
	p = subprocess.Popen(getMac, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read(100)
	print out
	wordList = out.split()
	return wordList[-1]

#returns polling value to webpage 	
@app.route('/_getReading')
def add_numbers():
	sensor = ORPI2C.ORPI2C()
	reading = sensor.poll()
	return jsonify(result=reading)

#app for advanced settings such as endpoint, devID, and security files	
@app.route("/advanced", methods=['GET', 'POST'])
def runAdvancedForm():
	form = AdvancedSetup()

	if request.method == 'POST':
		devId=request.form['devId']
		endpoint = request.form['endpoint']
		myPi.setMacAddr(getMacAddr())
		try:
			if 'rootca' in request.files:
				filename=files.save(request.files['rootca'])
				if 'root-CA' in filename:
					myPi.setRootCA(uploadDirectory + filename)
				elif myPi.getRootCA() =='':
					flash('root-CA.crt not uploaded. Do not modify ASW default file name.')
				else:
					flash("root-CA not updated. It was previously loaded and is set to " + myPi.getRootCA() + ".")
			if 'privatekey' in request.files:
				filename=files.save(request.files['privatekey'])
				if 'private' in filename:
					myPi.setPrivateKey(uploadDirectory + filename)
				elif myPi.getPrivateKey() == '':
					flash('private.pem.key not uploaded. Do not modify ASW default file name.')
				else:
					flash("private.pem.key not updated. It was previously loaded and is set to " + myPi.getPrivateKey() + ".")
			if 'certpem' in request.files:
				filename=files.save(request.files['certpem'])
				if 'certificate.pem' in filename:
					myPi.setCertPem(uploadDirectory + filename)
				elif myPi.getCertPem() =='':
					flash('certificate.pem.crt not uploaded. Do not modify ASW default file name.')
				else:
					flash("certificate.pem.crt not updated. It was previously loaded and is set to " + myPi.getCertPem() + ".")
		except:
			flash('If trying to upload files please upload all files at once.')
				
		if len(devId) == 10 and devId.isdigit():
			myPi.setName(devId)
		elif myPi.getName() == '':
			flash ('Device ID not set, must be 10 digit integer.')
		elif not myPi.getName() == '':
			flash ("Module ID was not updated, current ID is " + myPi.getName() +".")
		if 'amazonaws.com' in endpoint:
			myPi.setEndpoint(endpoint)
		elif myPi.getEndpoint() == '':
			flash ('AWS Endpoint not set and must be entered.')
		elif not myPi.getEndpoint() == '':
			flash ("Module endpoint was not updated, current endpoint is " + myPi.getEndpoint()+".")
			
	return render_template('advance.html', form=form)
	
#app for basic setup info like wifi connection and poll interval
@app.route("/", methods=['GET', 'POST'])
def runBasicForm():
	form = BasicSetup()

	#print form().errors
	if request.method == 'POST':
		queryInterval=request.form['queryInterval']
		ssid=request.form['ssid']
		password=request.form['password']
		checkConn=request.form['checkConn']
		
		#checks if connected to the designated ssid 
		if checkConn == 'checkConn':
			if isConnected():
				flash('Wifi is connected. ')
			else:
				flash('Wifi is not connected please allow more time or resubmit your settings.')
		#verifies form input
		if len(queryInterval) >= 1 and len(queryInterval) <= 2 and queryInterval.isdigit() and (int(queryInterval) >= 1 and int(queryInterval) <= 60):
			myPi.setMeasureInterval(queryInterval)
		elif myPi.getMeasureInterval() == '':
			flash('Poll interval not set. Please add value 1 to 60 minutes.')
		elif not queryInterval.isdigit():
			flash ('Query Interval not updated, must be an integer from 1 to 60.')
		elif queryInterval.isdigit():
			if (int(queryInterval) < 1 or int(queryInterval) > 60):
				flash ('Query Interval	must be an integer from 1 to 60.')
		if len(ssid) >= 1 and len(ssid) <= 35:
			myPi.setSSID(ssid)
			flash('Attempting to connect to' + ssid + '. Please check connection in about 1 minute.' )
		elif myPi.getSSID()== '':
			flash('SSID must be set to join WiFi network and upload data')	
		if not password == '':
			myPi.setPassword(password)
		elif myPi.getPassword() == '' and not ssid == '':
			flash('Password not set, assuming open encryption for ' + ssid + '. Please check connection in about 1 minute.')
		
	return render_template('form.html', form=form)
 
if __name__ == "__main__":
	#app.run()
	app.run(host= '0.0.0.0', port=5000)