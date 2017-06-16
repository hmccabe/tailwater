<?php 
include "../inc/dbinfo.inc";
session_start();
if (!isset($_SESSION['customer_id']) || empty($_SESSION['customer_id'])) {
  header("Location: login.php");
} else {
  $customer_id = $_SESSION["customer_id"];
}
?>

<html>

<head>
<link rel="stylesheet" type="text/css" href="./css/orp.css">
<title>Tailwater Systems</title>
</head>

<body>
<?php include "../inc/header.php";?>
<div style="text-align: center;">
<div id="container">   
<img src="img/tailwater.jpg" alt=""/>
<h2>ORP Data</h2>
<?php
  /* Connect to MySQL and select the database. */
  $connection = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD);
  if (mysqli_connect_errno()) echo "Failed to connect to MySQL: " . mysqli_connect_error();

  $database = mysqli_select_db($connection, DB_DATABASE);

$sensor_id = "";
$min_reading = "";
$max_reading = "";

if (isset($_POST["sensor_id"]) && !empty($_POST["sensor_id"])) {
  $sensor_id = $_POST["sensor_id"];
}
if (isset($_POST["min_reading"]) && !empty($_POST["min_reading"])) {
  $min_reading = $_POST["min_reading"];
}
if (isset($_POST["max_reading"]) && !empty($_POST["max_reading"])) {
  $max_reading = $_POST["max_reading"];
}
?>

<!-- Filter options -->
<form action="<?PHP echo $_SERVER['SCRIPT_NAME'] ?>" method="POST">
  <table border="0" id="table_options">
    <tr>
      <th>Sensor ID</td>
      <th>Min Reading</td>
      <th>Max Reading</td>
      <th> </th>
    </tr>
    <tr>
      <td><input type="number" value="<?php echo $sensor_id; ?>" name="sensor_id" min="0" max="9999999999" size="10" step="1"></td>
      <td><input type="number" value="<?php echo $min_reading; ?>" name="min_reading" step="0.1"></td>
      <td><input type="number" value="<?php echo $max_reading; ?>" name="max_reading" step="0.1"></td>
      <td><input type="submit" value="Filter"></td>
     </tr> 
  </table>
</form>

<br>

<!-- Display table data. -->
<table id="data_table">
  <tr>
    <th id="data_th"></td>
    <th id="data_th">Sensor ID</td>
    <th id="data_th">Timestamp</td>
    <th id="data_th">Reading</td>
  </tr>

<?php
$query = "SELECT * FROM data INNER JOIN systems ON systems.customer_id = ";
$query .= $customer_id;
$query .= " AND ";
$query .= "data.sensor_id = systems.sensor_id";

if ($sensor_id != "" || $min_reading != "" || $max_reading != "") {
  $query .= " WHERE ";

  if ($sensor_id != "") {
    $query .= " sensor_id == " . $sensor_id;
  }
  
  if ($min_reading != "") {
    if ($sensor_id != "") {
      $query .= " AND ";
    }
    $query .= "orp_value >= " . $min_reading;
  }
  if ($max_reading != "") {
    if ($sensor_id != "" || $min_reading != "") {
      $query .= " AND ";
    }
    $query .= "orp_value <= " . $max_reading;
  }
}

$query .= " ORDER BY timestamp DESC";

//echo $query . "<br><br>";

$result = mysqli_query($connection,$query); 

$row_counter = 1;

while($query_data = mysqli_fetch_row($result)) {
  echo "<tr>";
  echo "<td id=\"data_td\">",$row_counter,   "</td>";
  echo "<td id=\"data_td\">",$query_data[1], "</td>",
       "<td id=\"data_td\">",$query_data[3], "</td>",
       "<td id=\"data_td\">",$query_data[2], "</td>";
  echo "</tr>";
  $row_counter++;
}
?>

</table>

<?php
  mysqli_free_result($result);
  mysqli_close($connection);
?>
</div>
</div>
</body>
</html>
