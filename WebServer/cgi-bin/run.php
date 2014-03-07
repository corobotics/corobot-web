<?php
    header("content-type:text/plain");
    // Get the destination using GET
    $fileName = $_GET ["fileName"];
    $fileLocation = "/var/www/uploadModule/uploads/";
    chdir($fileLocation);
    $output = shell_exec("python3 $fileName");
    echo $output;
?>