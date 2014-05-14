<?php
    header ("content-type:application/json");
    error_reporting(E_ALL);
    // DEFINED variables.
    define ("ROOT","/var/www");
    chdir(ROOT);
    include_once 'includes/communication_details.php';

    // Create a TCP/IP socket
    $socket = socket_create(AF_INET, SOCK_STREAM, 0);
    if ($socket === false) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        $output = "Unable to create a socket. Error code : [$errorCode]. Error message : $errorMessage.";
        die ($output);
    }
    //echo "socket_create() passed. Socket created.\n";

    //echo "Attempting to connect to 'HOSTNAME' at port 'BROWSER_PORT'.\n";
    if (!(socket_connect($socket, HOSTNAME, BROWSER_PORT))) {
        $errorCode = socket_last_error();
        $errorMessage = socket_strerror($errorCode);
        $output = "Unable to connect to 'HOSTNAME' at port 'BROWSER_PORT'.";
        die ($output);
    }
    $response = '';
    $response = socket_recv($socket, $output, 4096,0);
    // If no response received.
    if (($response == 0) || (!$response))
        echo "null";
    else
        // Encode into JSON and send the output.
        echo (json_encode($output));
    socket_close($socket);
?>