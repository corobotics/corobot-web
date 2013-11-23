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
		<h3>Connection Status : <label id="errorCode">NOT-CONNECTED</label></h3>
        <h3>Total robots : <label id="robotCount">0</label></h3>
		<!--input type="submit" onclick="checkRobotStatus()" value="Get status"</input-->
		<table id="robotStatusTable" border=1>
			<thead><tr>
				<th>Robot Name</th>
				<th>Robot Status</th>
                <th>X-position</th>
                <th>Y-position</th>
			</tr></thead>
            <tbody>
                <tr>
                    <td>$robot-name</td>
                    <td>$robot-status</td>
                    <td>$robot-X-position</td>
                    <td>$robot-Y-position</td>
                </tr>
            </tbody>
		</table>
	</div>
</body>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
    	function communicate(){
    		$.getJSON("/cgi-bin/jsonTest.py", function (data){
                var output = $.parseJSON (data);
                $("#robotStatusTable td").parent().remove();
                if (output == null){
                    $("#robotStatusTable").append 
                    ("<tr><td>$robot-name</td><td>$robot-status</td><td>$robot-X-position</td><td>$robot-Y-position</td></tr>");                    
                    console.log ("No data");
                    $("#robotCount").text("0");
                    $("#errorCode").text("NOT-CONNECTED!");
                }
                else {
                    var count = 0;
                    $.each (output, function (key,val){
                        //console.log (key);
                        //console.log (val);
                        $("#robotStatusTable").append ("<tr><td>"+key+"</td><td>"+val[2]+"</td><td>"+val[3]+"</td><td>"+val[4]+"</td></tr>");
                        count += 1;
                        /*for (var i=0;i < val.length;i++){
                            console.log(val[i]);
                        }*/
                    });
                    $("#robotCount").text(count);
                    $("#errorCode").text("Connected...");                    
                }
            })
            .success( function(){
                $("#errorCode").text("Connected...");
            })
            .fail( function(){
                $("#errorCode").text("NOT-CONNECTED!");
            });

    		setTimeout ('communicate()',5000);
    	};

    	$(document).ready( function(){
    		communicate();
    	});
	</script>
</html>