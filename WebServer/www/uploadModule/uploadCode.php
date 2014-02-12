<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="../GenericWeb/css/style.css" type="text/css" />
    <title>Upload code page</title>
  </head>
  <body>
    <?php include "../include.php";
        error_reporting(E_ALL);
    ?>
    <form action="/cgi-bin/uploader.php" method="post" enctype="multipart/form-data">
    <div class="page">
      <div class="body">
        <h1>Upload your code</h1>
        <p>Upload one file at a time and kindly confirm your upload in your workspace.</p>
        <div id="container">
            <table>
                <tr>
                    <td>
                        <label for="uName">Username:</label>  
                    </td>
                    <td></td>
                    <td>
                        <input type="text" name="uName"  id="uName"/> 
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="passWord">Password:</label>  
                    </td>
                    <td>
                        
                    </td>
                    <td>
                        <input type="text" name="passWord"  id="passWord"/> 
                    </td>
                </tr>
                <tr>
                    <td><label>Upload File: </label></td>
                    <td>
                        
                    </td>
                    <td>
                        <input type="file" name="uploadFile" id="uploadFile"/> 
                    </td>
                    <td>
                        <input type="submit" name="uploadBtn" value="Upload">
                    </td>
                </tr>
            </table>
        </div>
      </div>
  </form>
    </body>
</html>
