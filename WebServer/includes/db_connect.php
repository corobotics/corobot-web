<?php
include_once 'config.php';
$db = new mysqli (HOST,USER,PASSWORD,DATABASE);
if ($db->connect_errno > 0)
    die ('Unable to connect to database [' . db->connect_error . ']');
echo 'Connected';
?>