<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="GenericWeb/css/style.css" type="text/css"/>
    <title>Welcome Corobots server</title>
  </head>
  <body>
    <?php include "./include.php";
        error_reporting(E_ALL);
    ?>
    <div class="body">
      <h1>Welcome to the RIT Corobot server!</h1>
        <p>
      	  Our robots are ready and waiting on the third floor of the Golisano
      	  building to help you with tasks that you define.  These robots are
      	  already capable of navigating the building and reporting back to you,
      	  it's up to you (and your program) to tell them what to do.
        </p>
          <ul>
      	    <li>See where the robots are right now <a href="./location.php">here.</a></li>
            <li>Get the API to start writing your code (to be announced).</li>
            <li>Log in to upload and deploy your code <a href="uploadModule/workspace.php">here</a></li>
          </ul>
        </p>
    </div>
  </body>
</html>