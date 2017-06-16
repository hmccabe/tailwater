AWS = require('aws-sdk');

AWS.config.region = 'us-west-2';
var topic = "updateshadow";
var iot = new AWS.Iot();
var iotdata = new AWS.IotData({endpoint: 'https://a31wvqhnklkbzd.iot.us-west-2.amazonaws.com'});
var topic = "updateshadow:";
var thing = "012345678";

var shadowinfo = JSON.stringify({"state": {"desired":{ "property": 1}}});
var params = {
	thingName: thing,
	payload: shadowinfo,
};

iotdata.updateThingShadow(params, function(err, data){
	if (err) {console.log(err, err.stack);}
});
