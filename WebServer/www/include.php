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
<div id="container">
	<div class="page">
	<div class="header">
	<ul>
		<li><a href="/index.php">Home</a></li>
		<li><a href="/location.php">Robot Location</a></li>
        <?php if (!$loggedIn): ?>
		  <li><a href="/login.php">Login</a></li>
        <?php endif; ?>
		<?php if ($loggedIn): ?> 
			<li><a href="uploadCode.php">Upload Code</a></li>
			<li><a href="workspace.php">My workspace (<?php echo $_SESSION['id'];?>)</a></li>
		<?php endif; ?>
		<li><a href="/status.php">Status</a></li>
		<?php if ($loggedIn): ?> 
			<li><a href="/deploy.php">Deploy</a></li>
		<?php endif; ?>
		<li><a href="/contact.php">Contact us</a></li>
		<?php if ($loggedIn): ?> 
			<li><a href="/includes/logout.php">Logout</a></li>
		<?php endif; ?>
	</ul>
</div>