<?php
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
    include_once 'includes/folder_config.php';
    sec_session_start();
?>

<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Corobotics logs</title>
    <link rel="stylesheet" href="/css/style.css" type="text/css" />
  </head>
  <body>
    <?php include "./include.php";
        error_reporting(E_ALL);
        if (logged_in_check($mysqli) == true) :
    ?>
      <h3>Click a log to download it.</h3>
        <ul>
          <li><a href="<?php echo ('logs/' . $_SESSION['id'] . '/' . $_SESSION['id'] .
          UPLOAD_LOG_FILE); ?>">Upload log</a></li>
          <li><p><a href="<?php echo ('logs/' . $_SESSION['id'] . '/' . $_SESSION['id'] . 
          WORKSPACE_DEPLOY_LOG_FILE); ?>">Workspace deploy log</a></li>
          <li><a href="<?php echo ('logs/' . $_SESSION['id'] . '/' . $_SESSION['id'] .
          DISPATCH_LOG_FILE); ?>">Dispatch log</a></li>
        </ul>
        <!-- ADMIN functions only -->
        <?php
          if (isset($_SESSION['admin'])) :    
        ?>
          <h3>Admin logs</h3>
          <table border=2;align=center;style="height:250%;border-style:solid;">
            <th>Filename</th>
            <th>Last updated</th>
            <tr>
              <td><a href="<?php echo ('logs/admin/' . UPLOAD_LOG_FILE_ADMIN); ?>">Upload log</a></td>
              <td><?php echo date("F d Y H:i:s", filemtime('logs/admin/' . UPLOAD_LOG_FILE_ADMIN)); ?></td>
            </tr>
            <tr>
              <td><a href="<?php echo ('logs/admin/' . WORKSPACE_DEPLOY_LOG_FILE_ADMIN); ?>">Workspace deploy log</a>
              <td><?php echo date("F d Y H:i:s", filemtime('logs/admin/' . WORKSPACE_DEPLOY_LOG_FILE_ADMIN)); ?></td>
            </tr>
            <tr>
              <td><a href="<?php echo ('logs/admin/' . DISPATCH_LOG_FILE_ADMIN); ?>">Dispatch log</a></td>
              <td><?php echo date("F d Y H:i:s", filemtime('logs/admin/' . DISPATCH_LOG_FILE_ADMIN)); ?></td>
            </tr>
            <tr>
              <td><a href="<?php echo ('logs/admin/' . STUDENT_DETAILS_FILE_ADMIN); ?>">Student details log</a></td>
              <td><?php echo date("F d Y H:i:s", filemtime('logs/admin/' . STUDENT_DETAILS_FILE_ADMIN)); ?></td>
            </tr>
            <tr>
              <td><a href="<?php echo ('logs/admin/' . LOGIN_ATTEMPTS_LOG_ADMIN); ?>">Login attempts log</a></td>
              <td><?php echo date("F d Y H:i:s", filemtime('logs/admin/' . LOGIN_ATTEMPTS_LOG_ADMIN)); ?></td>
            </tr>
        <?php endif; ?>
    <?php else : ?>
    <p>You are not authorized to access this page. Please <a href="login.php">login</a>.</p>
    <?php endif; ?>
  </body>
</html>