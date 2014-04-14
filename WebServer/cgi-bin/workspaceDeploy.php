<?php
    header("content-type:text/plain");
    // Get the destination using GET
    error_reporting(E_ALL);
    chdir("/var/www");
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
    sec_session_start();
    // Check if its an authorized login
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

    $fileName = $_GET ["fileName"];
    // Log file details.
    $logFileName = $id . '_workspaceDeployLog.txt';
    // Open the log file in append mode.
    $logFileHandler = fopen($logFileName, 'a') or die ('Cannot open log file' . $logFileName);
    // Write the following details - Current time, IP, file name.
    
    date_default_timezone_set('America/New York');
    $currentTimestamp = date ("Y-m-d H:i:s") . " " . date_default_timezone_get();
    $userIp = $_SERVER['REMOTE_ADDR'];
    $data = "'" . $currentTimestamp . "'::'" . $userIp . "'::'" . $fileName . "'";
    WORK HERE
    chroot(directory)
    shell_exec("cp $apiFolder");
    $output = trim(shell_exec("python3 $fileName"));
    echo $output;
    fwrite($logFileHandler, $data . "::'$output'\n");
    fclose($logFileHandler);
    header ("Location: " . $_SERVER['HTTP_REFERER']);
?> 