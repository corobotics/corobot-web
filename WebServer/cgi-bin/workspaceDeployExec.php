<?php
    header("content-type:text/plain");
    error_reporting(E_ALL);
    chdir("/var/www"); 
    include_once 'includes/functions.php';
    sec_session_start();
    if(isset($_SESSION['id'])){
        exec("php /usr/lib/cgi-bin/workspaceDeploy.php ".$_GET['fileName']." ".$_SESSION['id']." ".$_GET['args'].">/dev/null 2>/dev/null &");
    }else{
        echo "Unauthorized login";
        header ("Location: /login.py");
    }
?>
