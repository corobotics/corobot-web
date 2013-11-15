<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Robot Status Page</title>
    <link rel="stylesheet" href="GenericWeb/css/style.css" type="text/css" />
    <script type="text/javascript">
		var DELIM = ":";
		var ERROR_CODE = "E";
		var SUCCESS_CODE = "S";
		var xmlhttp = new XMLHttpRequest(); 		
		var isAjaxWorking = false;
		var url = "http://129.21.30.80/cgi-bin/status.py";
		function checkRobotStatus() {
			if(xmlhttp && !isAjaxWorking) {
				xmlhttp.open("GET", url, true);
				xmlhttp.onreadystatechange = function() {
						isAjaxWorking = false;
						if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
							var output = new String(xmlhttp.response);
							var data = output.split (DELIM);
							if (data[0] == ERROR_CODE) {
								document.getElementById ("error-code").innerHTML = "Error in communicaton";
							} else if (data[0] == SUCCESS_CODE) {
								document.getElementById ("error-code").innerHTML = "Connected...";
//							var robotName = temp.substr(0,index);
//							var robotStatus = temp.substr(index+1);
								var robotName = new String(data[1]);
								var robotStatus = new String (data[2]);
								document.getElementById (robotName).cells[0].innerHTML = robotName;
								document.getElementById (robotName).cells[1].innerHTML = robotStatus;
							}

						} else if(xmlhttp.readyState == 4 && xmlhttp.status > 200) {
								document.getElementById("error-code").innerHTML = "Something is wrong";
						}
					};
				isAjaxWorking = true;
				xmlhttp.send();
			}
			setTimeout("checkRobotStatus();",10000);
		}
	</script>
</head>

<body onload="checkRobotStatus()">
<?php include "include.php"; ?>
	<div><h2>Welcome</h2></div>
	<div>
		<h3>Connection Status : <label id="error-code">NOT-CONNECTED</label></h3>
		<input type="submit" onclick="checkRobotStatus()" value="Get status"</input>
		<table id="robotStatusTable" border=1>
			<thead><tr>
				<td>Robot Name</td>
				<td>Robot Status</td>
			</tr></thead>
			<tr id="ROBOT1">
				<td>$robotname</td>
				<td>$status</td>
			</tr>
		</table>
	</div>
</body>
</html>
