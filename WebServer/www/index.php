<!DOCTYPE html>

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title>Corobots Template</title>
        <link rel="stylesheet" href="GenericWeb/css/style.css" type="text/css" />
        <!--[if IE 7]>
          <link rel="stylesheet" href="css/ie7.css" type="text/css" />
        <![endif]-->
    </head>
    <body>
<!--
        <div class="page">
            <div class="header">
                <a href="index.html" id="logo"></a>
                <ul>
                    <li><a href="home.html">Home</a></li>
                    <li class="selected"><a href="index.html">Robot Location</a></li>
-->
                    <!--<li><a href="UploadModule/uploadcode.html">Upload Code</a></li>-->
<!--
                    <li><a href="UploadModule/workspace.html">Workspace</a></li>
                    <li><a href="contact.html">Contact</a></li>
		    <li><a href="status.html">Status</a></li>		
                </ul>
            </div>
-->
<?php include "include.php" ?>
            <div class="body">
               
                    <h1>index</h1>
                    <p>Corobots from Dart</p> 
                    <p>
                        <!--<button type="button" name="getRobotLocation" id="getData">Get Location</button>-->
                    </p>
                    <div id="container">
                        <p id="text"></p>
                    </div>

                    <div id="tableContent" class="CSSTableGenerator">
                    </div>   
                    <p><img src="70FloorPlan.png"/></p>

            </div>



            <script type="application/dart" src="ServiceAccess.dart">

            </script>
            <script src="https://dart.googlecode.com/svn/branches/bleeding_edge/dart/client/dart.js"></script>
    </body>
</html>
