<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
        <title>Status page</title>
    </head>
    <body>
    <?php include "./include.php"; 
        error_reporting(E_ALL); 
    ?>
    <!--h1>Server down for maintenance</h1-->
        <div>
            <table>
                <tr>
                    <td>
                        <h2>Current status of Corobots</h2>
                    </td>
                </tr>
                <tr>
                    <td>
                        Send/receive requests : <label id="requestStatus">ACTIVE</label>
                        <input type="submit" onclick="toggleCommunicateStatus()" id="toggleButton" value="Stop getting status" 
                        title="Click to toggle send/receive request status"</input>
                        Status refresh rate = <label id="refreshRate">5</label> seconds.
                    </td>
                </tr>                
            </table>
        </div>
    	<div>
    		<h3>Connection Status : <label id="errorCode">Not connected to server.</label></h3>
            <h3>Total robots : <label id="robotCount">0</label></h3>
    		<table id="robotStatusTable" border=1>
    			<thead><tr>
    				<th>Robot Name</th>
    				<th>Robot Status</th>
                    <th>X-position</th>
                    <th>Y-position</th>
                    <th>Destination</th>
    			</tr></thead>
                <tbody>
                    <tr>
                        <td>$robot-name</td>
                        <td>$robot-status</td>
                        <td>$robot-X-position</td>
                        <td>$robot-Y-position</td>
                        <td>$robot-destination</td>
                    </tr>
                </tbody>
    		</table>
    	</div>
    </body>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
        // Send receive status for communicate()
        communicateStatus = true;
        // Function to toggle the status of send/receive requests.
        function toggleCommunicateStatus(){
            // Send/receive status : ACTIVE
            if (getCommunicateStatus()) {
                communicateStatus = false;
                $("#requestStatus").text("STOPPED");
                $("#toggleButton").val("Start getting status");
            }
            // Send/receive status : STOPPED
            else {
                communicateStatus = true;
                $("#requestStatus").text("ACTIVE");
                $("#toggleButton").val("Stop getting status");
                // Call communicate method
                communicate();
            }
        }
        function getCommunicateStatus(){
            return communicateStatus;
        }
        // Function to communicate to the server to get the robot count. Output received is JSON.
    	function communicate(){
            // Check if communicate status is active or not.
            if (!getCommunicateStatus()) return;
        	$.getJSON("/cgi-bin/jsonOutput.py", function (data){
                var output = $.parseJSON (data);
                $("#robotStatusTable td").parent().remove();
                if (output == null){
                    $("#robotStatusTable").append 
                    ("<tr><td>$robot-name</td><td>$robot-status</td><td>$robot-X-position</td><td>$robot-Y-position</td><td>$robot-destination</td></tr>");                    
                    $("#robotCount").text("0");
                }
                else {
                    var count = 0;
                    $.each (output, function (key,val){
                        $("#robotStatusTable").append ("<tr><td>"+key+"</td><td>"+val[2]+"</td><td>"+val[3]+"</td><td>"+val[4]+"</td><td>"+val[5]+"</td></tr>");
                        count += 1;
                    });
                    $("#robotCount").text(count);
                }
            })
            .success( function(){
                $("#errorCode").text("Connected to server.");
            })
            .fail( function(){
                $("#errorCode").text("Not connected to server.");
            });
            // Call communicate every 5 seconds.
            var refreshRateTimeout = $("#refreshRate").text() * 1000;
    		setTimeout ('communicate()',refreshRateTimeout);
    	}; // End of communicate()

    	$(document).ready( function(){
    		communicate();
    	});
	</script>
</html>