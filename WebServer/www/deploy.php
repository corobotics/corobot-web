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
            <h3>NAV_TO.PY &ltDestination&gt : 
                <select name="destination" id="destination" required>
                </select>
                <!--input type="text" name="destination" id="destination"-->
            </h3>
            <button type="button" name="deploy" id="deploy">Deploy</button> 
            <button type="button" name="startServer" id="startServer">Start server</button>
            <a href="temp.py"><button type="button" name="downloadFile">Download sample file</button></a>
            <h4>Code status : <label id="codeStatus"></label></h4>
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
                done : console.log ("I sent data : " + $("#destination").val()),
                success : function(data){
                    $("#codeStatus").text (data)},
                fail : $("#codeStatus").text("Sorry! Communication error!")
            });
        });
        $("#startServer").click(function(){
            $.ajax({
                url : "/cgi-bin/startServer.py",
                success : function(data){
                    $("#codeStatus").text (data)},
                fail : $("#codeStatus").text("Sorry! Communication error!")
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