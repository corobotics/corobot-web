<?php
    error_reporting(E_ALL);
    header("content-type:text/plain");
    chdir("/var/www");
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();

    // Get the destination using GET
    $WAY_POINT = $_GET ["destination"];
    if (isset($_SESSION['id'])) {
        $id = $_SESSION['id'];
    }
    
    else { 
        echo "Unauthorized login";
        header ("Location: /login.php");
    }

    // Connection parameters
    $HOST = "vhost1.cs.rit.edu";
    $PORT = 56000;

    chdir('logs');
    // Check if the directory already exists. If not, create one.
    if (!is_dir ($id)) {
        mkdir ($id);
        echo "Created the dir";
    }
    chdir ($id);
    // Log file details.
    $logFileName = $id . '_deployLog.txt';
    
    // Open the log file in append mode.
    $logFileHandler = fopen($logFileName, 'a') or die ('Cannot open log file' . $logFileName);
    // Write the following details - Current time, IP, file name.
    date_default_timezone_set('EST');
    $currentTimestamp = date ("Y-m-d H:i:s") . " " . date_default_timezone_get();
    $userIp = $_SERVER['REMOTE_ADDR'];
    $data = "'" . $currentTimestamp . "'::'" . $userIp . "'::'" . $WAY_POINT . "'";

    // Create a TCP/IP socket
    $socket = socket_create(AF_INET, SOCK_STREAM, 0);
    if ($socket === false) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        fwrite($logFileHandler, $data . "::'Unable to create a socket. Error code : [$errorCode]. Error message : $errorMessage.'\n");
        fclose($logFileHandler);    
        die ("Unable to create a socket. Error code : [$errorCode]. Error message : $errorMessage.\n");
    }
    //echo "socket_create() passed. Socket created.\n";

    //echo "Attempting to connect to '$HOST' at port '$PORT'.\n";
    if (!(socket_connect($socket, $HOST, $PORT))) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        fwrite($logFileHandler, $data . "::'Unable to connect to '$HOST' at port '$PORT'.'\n");
        fclose($logFileHandler);    
        die ("Unable to connect to '$HOST' at port '$PORT'.\n");
    }
    //echo "socket_connect() passed. Socket connected.\n";
    $bytes_sent = socket_send($socket, $WAY_POINT, strlen($WAY_POINT), 0);
    if (($bytes_sent === 0) || ($bytes_sent === FALSE)) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        fwrite($logFileHandler, $data . "::'Unable to send data. Error code : [$errorCode]. Error message : $errorMessage.'\n");
        fclose($logFileHandler);
        die ("Unable to send data. Error code : [$errorCode]. Error message : $errorMessage.\n");
    }
    $response = '';
    /*  TO BE CHECKED
    1. 
    //while ($output = socket_read($socket, 1024)){
    //while (false != socket_recv($socket, $output, 10,MSG_WAITALL)) {
        if (($output != null) && ($output != ""))
            $response .= $output;
    }
    or 2.
    if (socket_recv ($socket, $data, 4096, MSG_WAITALL) === FALSE){
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        socket_close($socket);
        die ("Unable to receive data. Error code : [$errorCode]. Error message : $errorMessage.\n");
    }
    else {
        echo $data;
        socket_close($socket);
    }
        TO BE CHECKED
    */
    
    
    $response = socket_recv($socket, $output, 500,0);
    echo ($output);
    socket_close($socket);
    fwrite($logFileHandler, $data . "::'$output'\n");
    fclose($logFileHandler);
    
?>