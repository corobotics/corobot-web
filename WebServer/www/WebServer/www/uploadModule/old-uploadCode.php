<?php
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();
?>

<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
        <title>Upload code page</title>
    </head>
    <body>
        <?php include "include.php";
            error_reporting(E_ALL);
            if (logged_in_check($mysqli) == true) :
        ?>
        <form action="/cgi-bin/uploader.php" method="post" enctype="multipart/form-data" 
            id="uploadForm" onsubmit="return validateFileUpload();">
            <div class="body">
                <p>Upload one file at a time and kindly confirm your upload in your workspace.</p>
                <table>
                    <tr><td><label>Upload File: </label></td>
                        <td><input type="file" name="uploadFile" id="uploadFile"/></td>
                    </tr>
                    <tr><td></td><td><input type="submit" name="uploadBtn" value="Upload"></td></tr>
                </table>
                <p><a href="<?php echo "logs/" . $_SESSION['id'] . "/" . $_SESSION['id'] . "_uploadLog.txt" ?>">Download</a> upload log file</p>
            </div>
        </form>
        <?php else : ?>
            <p>You are not authorized to access this page. Please <a href="login.php">login</a>.</p>
        <?php endif; ?>
    </body>
    <script>
        function validateFileUpload () {
            var fileName = document.getElementById ('uploadFile').value;
            // Check if a file is uploaded or not.
            if (fileName == "") {
                alert ("Please upload a file and then click 'upload'");
                return false;
            }
            // Check file size.
            var file = document.getElementById ('uploadFile').files[0];
            if (file.size < 1) {
                alert ("Empty files not allowed.");
                document.getElementById ('uploadForm').reset();
                return false;
            }
            // Check the file extension.
            var extension = fileName.substring (fileName.lastIndexOf (".")+1);
            if (extension != "py") {
                alert ("Only python files allowed.");
                document.getElementById ('uploadForm').reset();
                return false;
            }
            else {
                alert ("File uploaded. Please check the logs.");
            }
        }
    </script>
</html>
