<?php
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();
     
    if (logged_in_check($mysqli) == true) {
        $loggedStatus = 'in';
        $loggedIn = true;
    } else {
        $loggedStatus = 'out';
        $loggedIn = false;
    }
?>

<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="/css/style.css" type="text/css"/>
    <title>Welcome to the Corobotics project</title>
  </head>
  <body>
    <?php include "include.php";
        error_reporting(E_ALL);
    ?>
    <div class="body">
      <h1>Welcome to the RIT Corobotics server!</h1>
        <p>
      	  Our robots are ready and waiting on the third floor of the Golisano
      	  building to help you with tasks that you define.  These robots are
      	  already capable of navigating the building and reporting back to you,
      	  it's up to you (and your program) to tell them what to do.
        </p>
          <ul>
      	    <li>See where the robots are right now <a href="location.php">here.</a></li>
            <li>Get the API to start writing your code (to be announced).</li>
            <?php if (!$loggedIn): ?>
              <li><a href="login.php">Login</a> to upload and deploy your code.</li>
            <?php endif; ?>
          </ul>
        </p>
    </div>
  </body>
</html>