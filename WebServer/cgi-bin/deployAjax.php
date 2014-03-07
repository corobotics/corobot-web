<?php
    error_reporting(E_ALL);
    header("content-type:text/plain");
    // Get the destination using GET
    $WAY_POINT = $_GET ["destination"];
    //$WAY_POINT = "RNDLab";
    //echo "<h3>Destination : $WAY_POINT</h3>\n";

    // Connection parameters
    $HOST = "vhost1.cs.rit.edu";
    $PORT = 56000;

    // Create a TCP/IP socket
    $socket = socket_create(AF_INET, SOCK_STREAM, 0);
    if ($socket === false) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        die ("Unable to create a socket. Error code : [$errorCode]. Error message : $errorMessage.\n");
    }
    //echo "socket_create() passed. Socket created.\n";

    //echo "Attempting to connect to '$HOST' at port '$PORT'.\n";
    if (!(socket_connect($socket, $HOST, $PORT))) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        die ("Unable to connect to '$HOST' at port '$PORT'.\n");
    }
    //echo "socket_connect() passed. Socket connected.\n";
    $bytes_sent = socket_send($socket, $WAY_POINT, strlen($WAY_POINT), 0);
    if (($bytes_sent === 0) || ($bytes_sent === FALSE)) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        die ("Unable to send data. Error code : [$errorCode]. Error message : $errorMessage.\n");
    }
    $response = '';
    /*  
    //while ($data = socket_read($socket, 1024)){
    //while (false != socket_recv($socket, $data, 10,MSG_WAITALL)) {
        if (($data != null) && ($data != ""))
            $response .= $data;
    }
    */
    $response = socket_recv($socket, $data, 500,0);
    echo ($data);
    socket_close($socket);
    
    /*
    //echo ("Message sent successfully.");
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
    */
?>