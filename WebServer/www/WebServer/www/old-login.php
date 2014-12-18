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
        <title>Secure Login: Log in to the Corobotics portal</title>
        <!--script type="text/JavaScript" src="js/sha512.js"></script--> 
        <script src="http://crypto-js.googlecode.com/svn/tags/3.1.2/build/rollups/sha512.js"></script>
        <script src="js/forms.js"></script> 
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
    </head>
    <body>
        <?php
            include "include.php";
            if (isset($_GET['error'])) {
                echo '<p>Error Logging In!</p>';
            }
        ?> 
        <form action="/includes/process_login.php" method="post" id="loginForm">                      
            <table>
                <tr>
                    <td>Test Id: </td>
                    <td><input type="text" name="id" id="id"/></td>
                </tr>
                <tr>
                    <td>Password: </td>
                    <td><input type="password" name="p" id="p"/></td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type="submit" value="Login" onclick="formhash(this.form,this.form.p);"/>
                    <input type="reset"/></td>
            </table>
        </form>
    </body>
</html>