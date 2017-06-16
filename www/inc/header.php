<?php session_start(); ?>

<div id="header">
<?php
if (isset($_SESSION["access_level"]) && !empty($_SESSION["access_level"])) {
  $access_level = (string)$_SESSION["access_level"];
  if ($access_level == "1") {
    echo ' | <a href="adduser.php">Add User</a>';
  }
}
?>
 | <a href="data.php">Past Data</a>
 | <a href="updateaccount.php">Update Account</a>
 | <a href="ShadowUpdate.php">Update Device</a>
 | <a href="logout.php">Log Out</a>
</div>
