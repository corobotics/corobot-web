#!/usr/bin/php
<?php
    error_reporting(E_ALL);
    chdir("/var/www");
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();

    if (isset($_SESSION['id'])) {
        $id = $_SESSION['id'];
    }
    
    else { 
        echo "Unauthorized login";
        header ("Location: /login.php");
    }
    chdir('logs');
    // Check if the log directory already exists. If not, create one.
    if (!is_dir ($id)) {
        mkdir ($id);
        //echo "Created the log dir for $id";
    }
    chdir ($id);

    // Upload file details.
    $uploadDir = '/var/www/uploads/' . $id . '/';
    // Check if the uploads directory already exists. If not, create one.
    if (!is_dir ($uploadDir)) {
        mkdir ($uploadDir);
        //echo "Created the upload dir for $id";
    }

    $fileName = basename($_FILES['uploadFile']['name']);
    $fileLocation = $uploadDir . $fileName;
    $fileType = $_FILES['uploadFile']['type'];
    $tempName = $_FILES['uploadFile']['tmp_name'];
    $fileSize = $_FILES['uploadFile']['size'];

    // Log file details.
    $logFileName = $id . '_uploadLog.txt';
    // Open the log file in append mode.
    $logFileHandler = fopen($logFileName, 'a') or die ('Cannot open log file' . $logFileName);
    // Write the following details - Current time, IP, file name.
    date_default_timezone_set('EST');
    $currentTimestamp = date ("Y-m-d H:i:s") . " " . date_default_timezone_get();
    $userIp = $_SERVER['REMOTE_ADDR'];
    $data = "'" . $currentTimestamp . "'::'" . $userIp . "'::'" . $fileName . "'";
    
    if ($fileSize < 1) {
        $status = "'Empty file'\n";
        fwrite($logFileHandler, $data . "::" . $status);
        fclose($logFileHandler);    
        die ('Empty files not allowed.');
    }
    
    if (($fileType != 'text/x-python-script') && ($fileType != 'text/x-python')) {
        $status = "'Invalid file type'\n";
        fwrite($logFileHandler, $data . "::" . $status);
        fclose($logFileHandler);
        die ('Only python file allowed.');
    }
    
    // File moved successfully.
    if (move_uploaded_file($tempName, $fileLocation)) {
        //echo "File uploaded successfully." . "<br />";
        chmod($fileName, 0777);
        //echo "File access changed to 644." . "<br />";

        $status = "'Upload success'\n";
        fwrite($logFileHandler, $data . "::" . $status);
    }

    // If unable to upload the file.
    else {
        echo 'Upload error = ' . $_FILES['uploadFile']['error'];
        $status = "'Upload error'\n";
        fwrite($logFileHandler, $data . "::" . $status);
        fclose($logFileHandler);
        die ("Unable to upload the file." . "<br />");
    }
    fclose($logFileHandler);
    header ("Location: " . $_SERVER['HTTP_REFERER']);
?> 