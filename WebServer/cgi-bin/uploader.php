<?php
    header("content-type:text/plain");
    error_reporting(E_ALL);

    // DEFINED variables.
    define ("ROOT","/var/www");

    chdir(ROOT);
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
    include_once 'includes/folder_setup.php';
    include_once 'inclues/db_names.php';

    // Check for unauthorized login.     
    sec_session_start();
    if (isset($_SESSION['id']))
        $id = $_SESSION['id'];
    else { 
        echo "Unauthorized login";
        header ("Location: /login.php");
    }

    // Allowed file types.
    $allowed_file_types = array("text/x-python-script","text/x-python","application/octet-stream");

    // Test to see if the folders and files exist or not.
    createFoldersAndFiles ($id);

    // CD to the $id's log folder.
    chdir (LOG_FOLDER);
    chdir ($id);

    // Upload file details.    
    $uploadDir =  UPLOAD_FOLDER . $id . '/';
    $fileName = basename($_FILES['uploadFile']['name']);
    $fileLocation = $uploadDir . $fileName;

    // AKSHAY - MAKE AN ARRAY OF ALLOWED FILE TYPES.
    $fileType = $_FILES['uploadFile']['type'];
    $tempName = $_FILES['uploadFile']['tmp_name'];
    $fileSize = $_FILES['uploadFile']['size'];

    // Log file details.
    $logFileName = $id . UPLOAD_LOG_FILE;
    // Open the log file in append mode.
    $logFileHandler = fopen($logFileName, 'a') or die ('Cannot open log file' . $logFileName);
    // Write the following details - Current time, IP, file name.
    date_default_timezone_set('America/New York');
    $currentTimestamp = date ("Y-m-d H:i:s") . " " . date_default_timezone_get();
    $userIp = $_SERVER['REMOTE_ADDR'];
    $data = "'" . $currentTimestamp . "'::'" . $userIp . "'::'" . $fileName . "'";
    
    if ($fileSize < 1) {
        $status = "Empty file";
        fwrite($logFileHandler, $data . "::'" . $status . "'\n");
        fclose($logFileHandler);    
        die ($status);
    }

    // Check for allowed file types.
    /*if (($fileType != 'text/x-python-script') && ($fileType != 'text/x-python') && 
        ($fileType != 'application/octet-stream')) {*/
    if (!in_array($fileType, $allowed_file_types,true)) {
        $status = "Invalid file type";
        fwrite($logFileHandler, $data . "::'" . $status . "'\n");
        fclose($logFileHandler);
        die ($status);
    }
    
    // File moved successfully.
    if (move_uploaded_file($tempName, $fileLocation)) {
        //echo "File uploaded successfully." . "<br />";
        //chmod($fileName, 0777);
        //echo "File access changed to 644." . "<br />";

        $status = "Upload success";
        fwrite($logFileHandler, $data . "::'" . $status . "'\n");
    }

    // If unable to upload the file.
    else {
        $error = 'Upload error = ' . $_FILES['uploadFile']['error'];
        fwrite($logFileHandler, $data . "::'" . $$error . "'\n");
        fclose($logFileHandler);
        die ($error . "<br />");
    }
    fclose($logFileHandler);

    // Write the log to the database
    if ($stmt = $mysqli->prepare("INSERT INTO " . UPLOAD_LOG_TABLE . 
        " (user_id, user_ip4, filename, output) VALUES " . 
        "(?,?,?,?)")) {
        $stmt->bind_param ('ssss',$_SESSION['id'], $userIp, $fileName, $status);
        $stmt->execute();
    }
    // Redirect back to the upload page.
    header ("Location: " . $_SERVER['HTTP_REFERER']);
?> 