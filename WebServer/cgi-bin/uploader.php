#!/usr/bin/php
<?php 
    error_reporting(E_ALL);
    $uploadDir = '/var/www/uploadModule/uploads/';
    $fileName = basename($_FILES['uploadFile']['name']);
    $fileLocation = $uploadDir . $fileName;
    $fileType = $_FILES['uploadFile']['type'];
    $tempName = $_FILES['uploadFile']['tmp_name'];
    echo "File name : $fileName." . "<br />";
    echo "File type : $fileType." . "<br />";
    if ($fileType != 'text/plain')
        die ('Only text uploads allowed.');
    
    echo "File location : $fileLocation." . "<br />";   
     
    // File moved successfully.
    if (move_uploaded_file($tempName, $fileLocation)) {
        echo "File uploaded successfully." . "<br />";
        //chmod($fileLocation, 0644);
        //echo 'File access changed to 644.' . <br />;
    }
    // If unable to upload the file.
    else {
        echo 'Upload error = ' . $_FILES['uploadFile']['error'];
        die ("Unable to upload the file." . "<br />");
    }
?>