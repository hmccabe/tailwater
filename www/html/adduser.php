<?php
  session_start();
?>

<html>
<head>
<link rel="stylesheet" type="text/css" href="../css/orp.css">
<title>Tailwater Systems</title>
</head>
<body>
<?php include "../inc/header.php"; ?>
<div style="text-align: center;">
div id="container">
<img src="img/tailwater.jpg" alt="" />
<h2>Add User</h2>
<form action="processadduser.php" method="POST">
  <table class="form_table">    
    <tr><th>Email:</th><td><input type="text" name="email"></td></tr>
    <tr><th>Password:</th><td><input type="password" name="password"></td></tr>
    <tr><th>Customer ID:</th><td><input type="number" step="1" min="0" name="cust_id"></td></tr>
    <tr><td colspan=2 align="right"><input type="submit" value="Submit"></td></tr>
  </table>
  </form>
</div>
</div>
</body>
</html>
