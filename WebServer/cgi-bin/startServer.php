<?php 
echo ("Starting server...");
$ret_code =system("sudo python /home/robotics/Desktop/gitWebServer/corobot-web/WebServer/serverCode/server.py", $retval);
echo $ret_code;
?>