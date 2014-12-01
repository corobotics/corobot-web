<?php
    error_reporting(E_ALL);
    header("content-type:text/plain");
    define ("ROOT", "/var/www");
    chdir(ROOT);
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
    include_once 'includes/folder_setup.php';
    include_once 'include/db_names.php';

    sec_session_start();

    if (isset($_SESSION['id'])){
        $id = $_SESSION['id'];
    }
    else {
        echo "Unauthorized login";
        header ("Location: /login.php");
    }

    chdir(LOG_FOLDER);
    chdir($id);
    $fileName = $_GET["fileName"];
    chmod($fileName, 0777);
    if( is_readable($fileName) ){
        unlink($fileName);
    }else {
        echo "NOPE";
    }
?>
