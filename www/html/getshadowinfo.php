<?php

function getShadow($thingName){
	//$thingName = $_POST['ThingName'];
	$data = "{\"thingID\":\"" . $thingName . "\" }";
	$ch = curl_init('https://phziv7cy36.execute-api.us-west-2.amazonaws.com/getshadowinfo/get-shadow-api');
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    	'Content-Type: application/json',
    	'Content-Length: ' . strlen($data))
	);
	sleep(5);
	$result = curl_exec($ch);
	return $result;
}

if (isset($_POST['ThingName'])){
        echo getshadow($_POST["ThingName"]);
}
?>
