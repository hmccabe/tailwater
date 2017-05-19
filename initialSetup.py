#Author; Matthew Mason
#Description: runs flask application to connect to Pi virtual ap in order to iniate settings for client connection and genernal operation

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import ConfigParser
import subprocess
from wifiSetup import isConnected
import time

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class PiForm():
	devId = TextField('Device Id:', validators=[validators.required()])
	queryInterval = TextField('Query Interval:', validators=[validators.required(), validators.Length(min=1, max=2)])
	password = TextField('Password:', validators=[validators.required()])
	ssid = TextField('Router SSID', validators=[validators.required(), validators.Length(min=1, max=35)])
	
#updates config file with new settings from web interface	
def updateConfig(devId, queryInterval, ssid, password, macaddr):
	
	config = ConfigParser.ConfigParser()
	config.read('device.cfg')
	
	
	config.set('DEVICE', 'NAME', devId)
	config.set('DEVICE', 'MEASURE', queryInterval) 
	config.set('DEVICE', 'SSID', ssid) 
	config.set('DEVICE', 'PASSWORD', password)
	config.set('DEVICE', 'MACADDR', macaddr)
	with open('device.cfg', 'wb') as configfile:
		config.write(configfile)

#get wifi client mac
def getMacAddr():
	getMac = "ifconfig wlan0 | grep HWaddr"
	p = subprocess.Popen(getMac, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read(100)
	print out
	wordList = out.split()
	return wordList[-1]
 
@app.route("/", methods=['GET', 'POST'])
def runForm():
	form = PiForm()
 
	#print form().errors
	if request.method == 'POST':
		devId=request.form['devId']
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
		#verife=ies form input
		elif len(devId) >= 1 and len(devId) <= 35 and len(queryInterval) >= 1 and len(queryInterval) <= 2 and len(ssid) >= 1 and len(ssid) <= 35:
			flash('Setup complete for ' + devId + '! We will attempt to associate with ' + ssid + '. Please check connect button in about 1 min.')
			updateConfig(devId, queryInterval, ssid, password, getMacAddr())
		elif not queryInterval.isdigit():
			flash ('Query Interval	must be an integer.')
		elif int(queryInterval) < 1 or int(queryInterval) > 60:
			flash ('Query Interval must be between 1 and 60.')
		else:
			flash('Error: Devce Id, Query Interval, and SSID are required. ')
			
	return render_template('form.html', form=form)
 
if __name__ == "__main__":
	#app.run()
	app.run(host= '0.0.0.0', port=5000)