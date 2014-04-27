<?php
    header("content-type:text/plain");
    error_reporting(E_ALL);
    // DEFINED variables.
    define ("ROOT","/var/www");
    define ("WORKSPACE_DEPLOY_LOG_TABLE", "workspace_deploy_log");

    chdir(ROOT);
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
    include_once 'includes/initial_setup.php';

    sec_session_start();
    // Check if its an authorized login
    if (isset($_SESSION['id'])) {
        $id = $_SESSION['id'];
    }
    else { 
        echo "Unauthorized login";
        header ("Location: /login.php");
    }

    // Location of the API folder. NOTE: It is not a PHP 'define' type, as we need to append
    // it with the extension of the file type.
    $API_FOLDER = "/var/www/api/";

    // Test to see if the folders and files exist or not.
    createFoldersAndFiles ($id);

    // CD to the $id's log folder.
    chdir(LOG_FOLDER);
    chdir ($id);

    // Extract the 'file name' from $_GET
    $fileName = $_GET ["fileName"];
    $fileType = substr(strrchr($fileName, '.'),1);

    // Set the appropriate variables based on the file-type.
    switch ($fileType) {
        case 'py':
            $fileType = "python";
            $executable = "python3";
            break;
        case 'java':
            $fileType = "java";
            $executable = "javac";
            break;
    }
    // Append the file-type for the respective API folder.
    $API_FOLDER .= $fileType;

    // Log file details.
    $logFileName = $id . WORKSPACE_DEPLOY_LOG_FILE;
    // Open the log file in append mode.
    $logFileHandler = fopen($logFileName, 'a') or die ('Cannot open log file' . $logFileName);
    // Write the following details - Current time, IP, file name.
    
    date_default_timezone_set('America/New York');
    $currentTimestamp = date ("Y-m-d H:i:s") . " " . date_default_timezone_get();
    $userIp = $_SERVER['REMOTE_ADDR'];
    $data = "'" . $currentTimestamp . "'::'" . $userIp . "'::'" . $fileName . "'";
    //WORK HERE
    //chroot(directory)
    chdir (UPLOAD_FOLDER);
    chdir ($id);
    shell_exec("cp -r $API_FOLDER/* .");
    if ($fileType == "python")
        $output = trim(shell_exec("python3 $fileName"));
    else if ($fileType == "java") {
        $output = exec("javac $fileName", $array, $returnVar);
        // Successful compilation.
        if ((!$output) || ($output == ""))
            echo "Successful compilation.";
        else {
            echo "javac output-> $output.";
            foreach ($array as $value) {
                echo "<br>$value";
            }
        }
        if (!$returnVar) {
            $executableName = substr($fileName,0,strpos($fileName, "."));
            //echo "<br>Executing $fileName";
            $output = exec("java $executableName", $array, $returnVar);
            /*
            echo "java $fileName output-> $output.";
            foreach ($array as $value) {
                echo "<br>$value";
            }
            */
        }
    }
    $output = str_replace("\n", ".", $output);
    echo $output;
    fwrite($logFileHandler, $data . "::'$output'\n");
    fclose($logFileHandler);

    // Write the log to the database
    if ($stmt = $mysqli->prepare("INSERT INTO " . WORKSPACE_DEPLOY_LOG_TABLE . 
        " (user_id, user_ip4, filename, output) VALUES " . 
        "(?,?,?,?)")) {
        $stmt->bind_param ('ssss',$_SESSION['id'], $userIp, $fileName, $output);
        $stmt->execute();
    }
    else
        header ('Location: /error.php?err="Unable to add details to the database"');
?> 