<?php 
  session_start();
  if (isset($_SESSION['customer_id']) && !empty($_SESSION['customer_id'])) {
    header("Location: data.php");
  }
  include "../inc/dbinfo.inc"; 
  $connection = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD);
  $database = mysqli_select_db($connection, DB_DATABASE);
  if (isset($_POST['email']) && !empty($_POST['email'])) {
    $email = $_POST['email'];
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);
    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
      $query = "SELECT password,customer_id,access_level FROM users WHERE email='" . $email . "'";  
      $result = mysqli_query($connection,$query);
      if (count($result) > 0) {
        $result = mysqli_fetch_row($result);
        $hash = $result[0];
        $password = $_POST['password'];
        if (password_verify($password,$hash)) {
          $customer_id = $result[1];
          $access_level = $result[2];
          $_SESSION["customer_id"] = (string)$customer_id;
          $_SESSION["access_level"] = (string)$access_level;
        }
      }
    }
  }
  mysqli_free_result($result);
  mysqli_close($connection);
  if (isset($_SESSION['customer_id'])) {
    header("Location: data.php");
  } else {
    header("Location: login.php");
  }
?>
