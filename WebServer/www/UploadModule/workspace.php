<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8">
        <title>uploadcode</title>
        <link rel="stylesheet" href="base.css">      
        <link rel="stylesheet" href="base.css">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="../GenericWeb/css/style.css" type="text/css" />
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
           <li><a href="../home.html">Home</a></li>
          <li><a href="../index.html">Robot Location</a></li>
-->
          <!--<li><a href="uploadcode.html">Upload Code</a></li>-->
<!--
          <li class="selected"><a href="workspace.html">Workspace</a></li>
          <li><a href="../contact.html">Contact</a></li>
        </ul>
      </div>
-->
<?php include "../include.php"; ?>
      <div class="body">
         <h1>Work Space</h1>

        <p>Welcome to corobots</p>

        <div id="container">
            <table >
                <tr>
                    <td>
                        <label for="uName">Username:</label>
                    </td>
                    <td width="33px"></td>
                    <td>
                        <input type="text" name="uName" label="User Name"  id="uName"/>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="pName">Password:</label>  
                    </td>
                    <td></td>
                    <td>
                        <input type="password" name="pName"  id="pName"/> 
                    </td>
                </tr>
                <tr>
                    <td><label>Upload File: </label></td>
                    <td>
                        
                    </td>
                    <td>
                        <input type="file" name="uploadFile" id="uploadFile"/> 
                    </td>
                </tr>
                <tr>
                    <td>
                    </td>
                    <td></td>
                    <td>
                        <button type="button" name="login" id="login">Show Workspace</button> 
                    </td>
                </tr>
                
            </table>
            <div id="tableContent" class="CSSTableGenerator">
            </div>
            <table>
                <tr>
                    <td>
                        <label for="fileList">Filenames:</label>  
                    </td>
                    <td></td>
                    <td>
                        <input type="text" name="fileList"  id="fileList"/>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="numFiles">Number of Files:</label>  
                    </td>
                    <td></td>
                    <td>
                        <input type="text" name="numFiles"  id="numFiles"/> 
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                    <td>
                        <button type="button" name="deploy" id="deploy">Deploy</button>
                    </td>
                </tr>
            </table>
        </div>
      </div>
         <p>
    
    </p>
       

        <script type="application/dart" src="myworkspace.dart"></script>
        <script src="https://dart.googlecode.com/svn/branches/bleeding_edge/dart/client/dart.js"></script>

    </body>
</html>