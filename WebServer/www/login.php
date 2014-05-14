<?php
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();
     
    if (logged_in_check($mysqli) == true) {
        $loggedStatus = 'in';
        header ("Location: index.php");
    } else {
        $loggedStatus = 'out';
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title>Secure Login: Log in to the Corobotics portal</title>
        <script src="js/forms.js"></script> 
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
    </head>
    <body>
        <?php
            include "include.php";
            if (isset($_GET['error'])) {
                header('Location: error.php?err=$_GET["error"]');
            }
        ?> 
        <form action="/includes/process_login.php" method="post" name="loginForm"
            onsubmit="return formhash(loginForm,loginForm.id,loginForm.p);">                      
            <table>
                <tr>
                    <td>RIT Id: </td>
                    <td><input type="text" name="id" id="id" style="text-transform:lowercase"/></td>
                </tr>
                <tr>
                    <td>Password: </td>
                    <td><input type="password" name="p" id="p"/></td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type="submit" value="Login">
                    <input type="reset"/></td>
            </table>
        </form>
    </body>
    <script type="text/javascript">
    document.getElementById('id').focus();
    </script>
</html>