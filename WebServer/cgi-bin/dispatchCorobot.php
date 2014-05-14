<?php
    header("content-type:text/plain");
    error_reporting(E_ALL);
    // DEFINED variables.
    define ("ROOT","/var/www");
    chdir(ROOT);
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
    include_once 'includes/folder_setup.php';
    include_once 'includes/db_names.php';
    include_once 'includes/communication_details.php';

    sec_session_start();
    // Get the destination using GET
    $WAY_POINT = $_GET ["destination"];
    if (isset($_SESSION['id']))
        $id = $_SESSION['id'];
    
    else { 
        echo "Unauthorized login";
        header ("Location: /login.php");
    }

    // Test to see if the folders and files exist or not.
    createFoldersAndFiles ($id);

    // CD to the $id's log folder.
    chdir (LOG_FOLDER);
    chdir ($id);

    // Log file details.
    $logFileName = $id . DISPATCH_LOG_FILE;
    
    // Open the log file in append mode.
    $logFileHandler = fopen($logFileName, 'a') or die ('Cannot open log file' . $logFileName);
    // Write the following details - Current time, IP, file name.
    date_default_timezone_set('America/New York');
    $currentTimestamp = date ("Y-m-d H:i:s") . " " . date_default_timezone_get();
    $userIp = $_SERVER['REMOTE_ADDR'];
    $data = "'" . $currentTimestamp . "'::'" . $userIp . "'::'" . $WAY_POINT . "'";
    
    // Create a TCP/IP socket
    $socket = socket_create(AF_INET, SOCK_STREAM, 0);
    if ($socket === false) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        $output = "Unable to create a socket. Error code : [$errorCode]. Error message : $errorMessage.";
        fwrite($logFileHandler, $data . "::'" . $output . "'\n");
        fclose($logFileHandler);    
        die ($output);
    }
    //echo "socket_create() passed. Socket created.\n";

    //echo "Attempting to connect to 'HOSTNAME' at port 'CLIENT_PORT'.\n";
    if (!(socket_connect($socket, HOSTNAME, CLIENT_PORT))) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        $output = "Unable to connect to 'HOSTNAME' at port 'CLIENT_PORT'.";
        fwrite($logFileHandler, $data . "::'" . $output . "'\n");
        fclose($logFileHandler);    
        die ($output);
    }
    //echo "socket_connect() passed. Socket connected.\n";
    $bytes_sent = socket_send($socket, $WAY_POINT, strlen($WAY_POINT), 0);
    if (($bytes_sent === 0) || ($bytes_sent === FALSE)) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        $output = "Unable to send data. Error code : [$errorCode]. Error message : $errorMessage.";
        fwrite($logFileHandler, $data . "::'" . $output . "'\n");
        fclose($logFileHandler);
        die ($output);
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

    // Write the log to the database
    if ($stmt = $mysqli->prepare("INSERT INTO " . DISPATCH_LOG_TABLE . 
        " (user_id, user_ip4, waypoint_name, output) VALUES " . 
        "(?,?,?,?)")) {
        $stmt->bind_param ('ssss',$_SESSION['id'], $userIp, $WAY_POINT, $output);
        $stmt->execute();
    }
?>