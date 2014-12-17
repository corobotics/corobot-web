<?php
    /*header("HTTP/1.1 302 Moved temporarily");
    header("Location : /maintenance.php");
    die();*/
    include_once 'includes/db_connect.php';
    include_once 'includes/functions.php';
     
    sec_session_start();
?>

<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<meta content = "utf-8" http-equiv="encoding"/>
        <link rel="stylesheet" href="/css/style.css" type="text/css" />
        <title>My workspace</title>
    </head>
    <body>
        <?php include "include.php";
            error_reporting(E_ALL);
            if (logged_in_check($mysqli) == true) :
        ?>
        <div style="width:940px;margin:0 auto;">
            <form action="/cgi-bin/uploader.php" method="post" enctype="multipart/form-data" 
                name="uploadForm" id="uploadForm" onsubmit="return validateFileUpload();">
                <p>Upload one file at a time and kindly confirm your upload in your workspace and logs.</p>
                <table>
                    <tr><td><label>Upload File: </label></td>
                        <td><input type="file" name="uploadFile" id="uploadFile"/></td>
                    </tr>
                    <tr><td></td><td><input type="submit" name="uploadBtn" value="Upload"></td></tr>
                </table>
            </form>
            <h3>List of my files</h3>
            <div style="height:400px;overflow:scroll;overflow-y:scroll;overflow-x:hidden;">
                <table border=2;align=center;style="height:250%;border-style:solid;">
                    <th>Upload timestamp</th>
                    <th>File Name</th>
		    <th>Arguments</th>
                    <th></th>
                    <?php
                        $fileLocation = 'uploads/' . $_SESSION['id'];
                        chdir($fileLocation);
                        $files = glob ("*.{java,py}", GLOB_NOSORT+GLOB_BRACE);
                        //usort($files, create_function('$a,$b', 'return filemtime($b) - filemtime($a);'));
                        array_multisort(array_map('filemtime', $files), SORT_NUMERIC, SORT_DESC, $files);
                        foreach ($files as $fileName) {
                            echo "<tr><td>" . date("F d Y H:i:s", filemtime($fileName)) . "</td><td><a href='$fileLocation/$fileName'>" . $fileName . "</a></td>";
			    echo "<td><input type = 'text' name = '$fileName'></td>";
                            echo "<td><button type='submit' value='$fileName' class='deployFileName'>Deploy</button></td></tr>";
                        }
                        chdir("../..");
                    ?>
                </table>
                <br>
		<h4>List of Log files</h4>
                <table border = 2; align=center; style="border-style:solid;">
                     <th>Log timestamp</th>
                     <th>File Run</th>
                     <th></th>
                     <?php
                         $fileLocation = 'logs/' . $_SESSION['id'];
                         chdir($fileLocation);
                         $files = glob ("*_log.txt", GLOB_NOSORT+GLOB_BRACE);
                         array_multisort(array_map('filemtime', $files), SORT_NUMERIC, SORT_DESC, $files);
                         foreach ($files as $fileName) {
                             echo "<tr><td>" .date("F d Y H:i:s", filemtime($fileName)) . "</td><td><a href= '$fileLocation/$fileName'>" .$fileName . "</a></td>";
                             echo "<td><button type='submit' value='$fileName' class = 'removeFileName'>Delete</button></td></tr>";
                         }
                     ?>
                </table>
            </div>
        <strong>NOTE</strong> : <ol><li>The output might need a couple of minutes to be displayed.</li>
        <li>You might see some extra API files in your workspace.</li></ol>
        </div>

        <?php else : ?>
            <p>You are not authorized to access this page. Please <a href="login.php">login</a>.</p>
        <?php endif; ?>
    </body>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
        // Function to validate file upload - Javascript
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
            
            if ((extension != "py") && (extension != "java")) {
                alert ("Only Python and Java files allowed.");
                document.getElementById ('uploadForm').reset();
                return false;
            }
            else 
                alert ("File submitted for upload.");
        }

        // Function to deploy a file from workspace -JQuery.
        $(function(){
            $('.deployFileName').on("click", function(){
                var fileName = $(this).val();
		var args = $("[name = '"+ fileName+"']").val();
		$.ajax({
		   url : "/cgi-bin/workspaceDeployExec.php",
		   data : "fileName=" + fileName + "&args="+ args,
		   type : "GET",
		   dataType: "text",
		   cache : false,
		   success : function(data){
                        alert("Program Submitted");
		   },
                   fail : function(data){
			alert("Sorry! Unable to deploy. Please contact the administrator.")},
                   complete : function(){ 
                       location.reload();},
                });
            });
            $('.removeFileName').on("click", function(){
                var fileName = $(this).val();
                $.ajax({
		   url : "/cgi-bin/workspaceDelete.php",
                   data: "fileName=" + fileName,
                   type: "GET",
                   dataType: "text",
                   complete: function(){
                       location.reload();},
                });
            });
        });

    </script>
</html>
