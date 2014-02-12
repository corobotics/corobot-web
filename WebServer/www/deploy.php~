<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Deploy code page</title>
        <link rel="stylesheet" href="GenericWeb/css/style.css" type="text/css" />
    </head>

    <body>
    <?php include "include.php"; ?>
    <h2>[Page under construction]</h2>
        <div>
            <!--h3>Enter the destination : <input type="text"> 
            </h3-->
            <h3>NAV_TO.PY &ltDestination&gt : <input type="text" name="destination" id="destination"></h3>
            <button type="button" name="deploy" id="deploy">Deploy</button> 
            <button type="button" name="startServer" id="startServer">Start server</button>
            <h4>Code status : <label id="codeStatus"></label></h4>
        </div>
    </body>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
        $("#deploy").click(function(){
            //console.log ($("#destination").val());
            
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
    </script>
</html>