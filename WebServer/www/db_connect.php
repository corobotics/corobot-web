<?php
printf("Trying to connect.");
$db = new mysqli('localhost','robotics','','login_info');

if ($db->connect_errno > 0) 
    die ('Unable to connect to database [' . $db->connect_error . ']');
echo nl2br("\nConnected");
$query = <<<SQL
    SELECT COUNT(*) FROM `student_info`
    WHERE id = "arj9065" AND
    password = "akshay"
SQL;

if (!$result = $db->query($query))
    die ('There was an error running the query [' . $db->error . ']');
while ($row = $result->fetch_assoc())
    echo "<pre>" . print_r($row) . "</pre>";

$db->close();

?>