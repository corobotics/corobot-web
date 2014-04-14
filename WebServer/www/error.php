<?php
    $error = filter_input(INPUT_GET, 'err', $filter = FILTER_SANITIZE_STRING);
     
    if (! $error) {
        $error = 'Oops! An unknown error happened.';
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Corobotics Login: Error</title>
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
    </head>
    <body>
        <h1><?php echo $error;?></h1>
        Go back to <a href="login.php">Login</a> page.
    </body>
</html>