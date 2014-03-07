<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Deploy code page</title>
        <link rel="stylesheet" href="./GenericWeb/css/style.css" type="text/css" />
    </head>
    <body>
    <?php include "./include.php";
        error_reporting(E_ALL);
    ?>
    <!--h1>Server down for maintenance</h1-->
        <div>
            <!--h3>NAV_TO.PY &ltDestination&gt : -->
            <h3>Select a destination : 
                <select name="destination" id="destination" required>
                </select>
                <!--input type="text" name="destination" id="destination"-->
            </h3>
            <button name="deploy" id="deploy">Deploy</button> 
            <button name="startServer" id="startServer">Start server</button>
            <a href="temp.py"><button type="button" name="downloadFile">Download sample file</button></a>
            <h4>Status : <label id="status"></label></h4>
        </div>
    </body>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
        var waypointsFileLocation = "./waypoints.txt";
        $("#deploy").click(function(){
            $.ajax({
                url : "/cgi-bin/deployAjax.php",
                data :  "destination=" + $("#destination").val(),
                type : "GET",
                dataType : "text",
                done : console.log ("Destination : " + $("#destination").val()),
                success : function(data){
                    $("#status").text (data)},
                fail : $("#status").text("Sorry! Communication error!")
            });
        });

        $("#startServer").click(function(){
            $.ajax({
                url : "/cgi-bin/startServer.py",
                success : function(data){
                    $("#status").text (data)},
                fail : $("#status").text("Sorry! Communication error!")
            });
        });
        $(window).load(function(){
            $.get(waypointsFileLocation, function(data){
                var lines = data.split("\n");
                $.each (lines, function(index, waypointName){
                    $("#destination").append ("<option value="+waypointName+">"+waypointName+"</option>");
                })
            })
        });
    </script>
</html>