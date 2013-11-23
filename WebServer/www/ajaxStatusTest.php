<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Robot Status Page</title>
    <link rel="stylesheet" href="GenericWeb/css/style.css" type="text/css" />
</head>

<body>
<?php include "include.php"; ?>
	<div><h2>Welcome</h2></div>
	<div>
		<h3>Connection Status : <label id="error-code">NOT-CONNECTED</label></h3>
		<!--input type="submit" onclick="checkRobotStatus()" value="Get status"</input-->
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
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
    	function communicate(){
    		$.ajax({
				url : "/cgi-bin/status.py",
				success : function (data){
					var response = data.split(":");
					var responseCode = response[0];
					var robotname = response[1];
					var robotStatus = response[2];
					if (responseCode == "S") {
						$('#robotStatusTable').append ('<tr><td>'+robotname+'</td><td>'+robotStatus+'</td></tr>');
						$('#error-code').text ("Connected...");
					}
					else if (responseCode == "E") 
						$('#error-code').text ("Error in communication!");
					else
						$('#error-code').text ("Invalid response code received");
				}
			});
    		setTimeout ('communicate()',4000);
    	};

    	$(document).ready( function(){
    		communicate();
    	});
	</script>
</html>