<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="../GenericWeb/css/style.css" type="text/css" />
    <title>Workspace</title>
  </head>
  <body>
    <?php include "../include.php";
        error_reporting(E_ALL);
    ?>
    <div class="body">
      <h1>Work Space</h1>
    <div id="container">
        <table>
            <tr>
                <td><label for="uName">Username:</label></td>
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

