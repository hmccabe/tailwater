<?php
session_start();
if (isset($_SESSION['customer_id']) && !empty($_SESSION['customer_id'])) {
  $customer_id = $_SESSION['customer_id'];
} else {
  header("Location: login.php");
}
?>
<html>
<head>
<meta charset="utf-8">
<title>Tailwater Systems </title>
<link rel="stylesheet" type="text/css" href="css/shadow.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<script type="text/javascript">
    $(document).ready(function(){
        $("#reading").click(function(){
                if($("#ThingName").val()== "" || $("#ThingName").val().length !== 10){
                        alert("Thing Name must be integer length 10!");
                }
                else{
			var response;
			$.ajax({
                        type: "POST",
			url: 'updateorpval.php',
			data: { "ThingName" : $("#ThingName").val(), "orpval": "ffff"},
			success: function (msg) {
			if(msg == 'null'){
					$("#MyEdit").text("Standby, this will take only a moment!");
					$.ajax({
					type: "POST",
					url: 'getshadowinfo.php',
					data: { "ThingName" : $("#ThingName").val()},
					success: function (msg) {
					parse1 = JSON.parse(msg)
					parse2 = JSON.parse(parse1.payload);
					$("#MyEdit").text("Current ORP Reading: " + parse2.state.reported.orpval);
					}
					});
				}
			else{
				alert(response);
			}	
		}
		});
		}
	});

	$("#update").click(function(){
                if($("#ThingName").val()== "" || $("#ThingName").val().length !== 10){

                        alert("Thing Name must be integer length 10!");
                }
		else if ($("#PollInterval").val() > 60 || $("#PollInterval").val() < 1){
			alert("Poll Interval must be between 1 and 60 minutes"); 
	         }else{
                        $.ajax({
                                type: "POST",
                                url: 'updatepollinterval.php',

                                data: { "ThingName" : $("#ThingName").val(), "PollInterval" : $("#PollInterval").val()},
                                success: function (msg) {

                                if(msg == "null"){
					$("#MyEdit").text($("#ThingName").val() + " has been updated!");
				}
				else{
					$('#MyEdit').text("Error: " +  $("#ThingName").val() + " was not updated please verify Thing Name.");
                                }
				}
                        });
                }



        });
});
</script>
</head>
<body>
<?php include "../inc/header.php"; ?>
<div id="container">
	<img src="img/tailwater.jpg" alt=""/>
        <h3> Thing Shadow Update</h3>
        <div class="form-group">
                <form id="ThingShadowUpdate">
                <table>
                        <tr>
                                <td id="labels"><label>Thing Name: </label></td>
                                <td id="userentry"><input type="number" id="ThingName" name="ThingName" maxlength="10" size"15" placeholder="Enter Thing ID" required></td>
                        </tr>
                        <tr>
                                <td id="labels"><label>Poll Interval: </label></td>
                                <td id="userentry"><input type="number" id="PollInterval" name="PollInterval"  min="1" max="60" value="15" required></td>
                        </tr>
                </table>
		<br>
                        <button type="button" id="update" name="update" value="update">Update Shadow</button>
                        <button type="button" id="reading" name="reading" value="reading">Get ORP Reading</button>

                </form>
        </div>
		<h4><div id="MyEdit">
		</div></h4>
</div>
</body>
</html>

