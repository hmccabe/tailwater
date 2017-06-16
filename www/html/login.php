<?php
  session_start();
  if (isset($_SESSION['customer_id']) && !empty($_SESSION['customer_id'])) {
    header("Location: data.php");
  }
?>

<html>
<head>
<link rel="stylesheet" type="text/css" href="../css/orp.css">
<title>Tailwater Systems</title>
</head>

<body>
<div style="text-align: center;">
<div id="container">
<img src="img/tailwater.jpg" alt="" />
<form action="processlogin.php" method="POST">
  <table id="login_table">    
    <tr><th>Email:</th><td><input type="text" name="email" size="20"></td></tr>
    <tr><th>Password:</th><td><input type="password" name="password" size="21"></td></tr>
    <tr><td colspan=2 align="right"><input type="submit" value="Submit"></td></tr>
  </table>
  </form>
</div>
</div>
</body>
</html>
