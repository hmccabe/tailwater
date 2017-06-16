<?php

function updateshadow($thingName, $orpval){
        
        $data = "{\"orpval\": \"" . $orpval . "\", \"thingName\":\"" . $thingName . "\" }";
        $ch = curl_init('https://fkmwegwpsc.execute-api.us-west-2.amazonaws.com/updateorpval/update-orp-val');
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
        echo updateshadow($_POST["ThingName"], $_POST["orpval"]);
}
?>
