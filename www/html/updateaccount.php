<html>
<head>
<link rel="stylesheet" type="text/css" href="../css/orp.css">
<title>Tailwater Systems</title>
</head>
<body>
<?php include "../inc/header.php"; ?>
<div style="text-align: center;">
<div id="container">
<img src="img/tailwater.jpg" alt="" />
<h2>Account Update</h2>
<form action="processnewuser.php" method="POST">
  <table class="form_table">    
    <tr><th>New Email:</th><td><input type="text" name="email" size="20"></td></tr>
    <tr><th>Current Password:</th><td><input type="password" name="current_password" size="21"></td></tr>
    <tr><th>New Password:</th><td><input type="password" name="current_password" size="21"></td></tr>
    <tr><th>Re-Enter New Password:</th><td><input type="password" name="current_password" size="21"></td></tr>
    <tr><td colspan=2 align="right"><input type="submit" value="Submit"></td></tr>
  </table>
  </form>
</div>
</div>
</body>
</html>
