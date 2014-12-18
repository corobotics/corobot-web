<?php
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();
/*
    echo "<pre>";
        print_r($_SESSION);
    echo "</pre>";
*/
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Secure Login: Corobotics protected Page</title>
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
    </head>
    <body>
    <?php include "./include.php";
        if (logged_in_check($mysqli) == true) : ?>
            <p>Welcome <?php echo htmlentities($_SESSION['id']); ?>!</p>
            <p>
                This is an example protected page.  To access this page, users
                must be logged in.  At some stage, we'll also check the role of
                the user, so pages will be able to determine the type of user
                authorised to access the page.
            </p>
            <a href="includes/logout.php">Logout</a>
        <?php else : ?>
            <p>You are not authorized to access this page. Please <a href="login.php">login</a>.
            </p>
        <?php endif; ?>
    </body>
</html>