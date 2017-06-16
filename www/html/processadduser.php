<?php 
  session_start();
  if (!isset($_SESSION['customer_id']) || empty($_SESSION['customer_id'])) {
    header("Location: login.php");
  }
  include "../inc/dbinfo.inc"; 
  $connection = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD);
  $database = mysqli_select_db($connection, DB_DATABASE);
  if (isset($_POST['email']) && !empty($_POST['email'])) {
    $email = $_POST['email'];
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);
    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
      if (isset($_POST['password']) && !empty($_POST['password'])) {
        $password = $_POST['password'];
        $password = password_hash($password, PASSWORD_DEFAULT, ["cost" => 10]);
        if (isset($_POST['cust_id']) && !empty($_POST['cust_id'])) {
          $cust_id = $_POST['cust_id'];
          $query = "INSERT INTO users (email,password,customer_id)";
          $query .= " VALUES (";
          $query .= "'" . $email . "',";
          $query .= "'" . $password . "',";
          $query .= $cust_id;
          $query .= ")";
          //echo $query; 
          $result = mysqli_query($connection,$query);
        }
      }
    }
  } 
  mysqli_free_result($result);
  mysqli_close($connection);
  header("Location: adduser.php");
?>
