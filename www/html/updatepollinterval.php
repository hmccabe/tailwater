<?php

function updateshadow($thingName, $pollInterval){
        
        $data = "{\"pollInterval\": \"" . $pollInterval . "\", \"thingName\":\"" . $thingName . "\" }";
        $ch = curl_init('https://ihh4jaogw9.execute-api.us-west-2.amazonaws.com/UpdateShadowV1/updateshadow');
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json',
        'Content-Length: ' . strlen($data))
        );
        $result = curl_exec($ch);
        return $result;
}

if (isset($_POST['ThingName'])){
        echo updateshadow($_POST["ThingName"], $_POST["PollInterval"]);
}
?>
