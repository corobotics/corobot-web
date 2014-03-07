#!/usr/bin/php
<?php
    error_reporting(E_ALL);
    // Upload file details.
    $uploadDir = '/var/www/uploadModule/uploads/';
    $fileName = basename($_FILES['uploadFile']['name']);
    $fileLocation = $uploadDir . $fileName;
    $fileType = $_FILES['uploadFile']['type'];
    $tempName = $_FILES['uploadFile']['tmp_name'];
    $fileSize = $_FILES['uploadFile']['size'];

    // Log file details.
    $logFileName = $uploadDir . 'uploadLog.txt';
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
    if ($fileSize < 1) {
        $status = "'Empty file'\n";
        fwrite($logFileHandler, $data . "::" . $status);
        fclose($logFileHandler);    
        die ('Empty files not allowed.');
    }
    
    //echo "File location : $fileLocation." . "<br />";   
     
    // File moved successfully.
    if (move_uploaded_file($tempName, $fileLocation)) {
        //echo "File uploaded successfully." . "<br />";
        chmod($fileLocation, 0777);
        //echo "File access changed to 644." . "<br />";

        // Execute the file.
        /*
        $output = shell_exec("python3 $fileLocation");
        echo "Output->" . $output;
        */
        $status = "'Upload success'\n";
        fwrite($logFileHandler, $data . "::" . $status);
    }

    // If unable to upload the file.
    else {
        //echo 'Upload error = ' . $_FILES['uploadFile']['error'];
        $status = "'Upload error'\n";
        fwrite($logFileHandler, $data . "::" . $status);
        fclose($logFileHandler);
        die ("Unable to upload the file." . "<br />");
    }
    fclose($logFileHandler);
?>