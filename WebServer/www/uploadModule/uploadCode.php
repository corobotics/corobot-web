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
        <form action="/cgi-bin/uploader.php" method="post" enctype="multipart/form-data" onsubmit="return validateFileUpload();">
            <div class="body">
                <p>Upload one file at a time and kindly confirm your upload in your workspace.</p>
                <table>
                    <tr><td><label>Upload File: </label></td>
                        <td><input type="file" name="uploadFile" id="uploadFile"/></td>
                    </tr>
                    <tr><td></td><td><input type="submit" name="uploadBtn" value="Upload"></td></tr>
                    <!--tr><td></td><td><button id="uploadBtn">Upload</button></td></tr-->
                </table>
            </div>
        </form>
    </body>
    <script>
        function validateFileUpload () {
            var fileName = document.getElementById ('uploadFile').value;
            // Check if a file is uploaded or not.
            if (fileName == "") {
                alert ("Please upload a file and then click 'upload'");
                return false;
            }
            // Check the file extension.
            var extension = fileName.substring (fileName.lastIndexOf (".")+1);
            if (extension != "py") {
                alert ("Only python files allowed.");
                return false;
            }
            else {
                alert ("File uploaded successfully.");
            }
        }
    </script>
</html>
