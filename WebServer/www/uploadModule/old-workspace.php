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
    <title>My workspace</title>
  </head>
  <body>
    <?php include "include.php";
        error_reporting(E_ALL);
        if (logged_in_check($mysqli) == true) :
    ?>
    <div style="width:940px;margin:0 auto">
        <h3>List of my files</h3>
        <table border=1;align=center>
            <th>Upload timestamp</th>
            <th>File Name</th>
            <th>Operation</th>
            <?php
                $fileLocation = 'uploads/' . $_SESSION['id'];
                chdir($fileLocation);
                

                // AKSHAY - check here, if extension is required or we can display all the files.


                $files = glob ("*.py", GLOB_NOSORT);
                //usort($files, create_function('$a,$b', 'return filemtime($b) - filemtime($a);'));
                array_multisort(array_map('filemtime', $files), SORT_NUMERIC, SORT_DESC, $files);
                foreach ($files as $fileName) {
                    echo "<tr><td>" . date("F d Y H:i:s", filectime($fileName)) . "</td><td><a href='$fileLocation$fileName'>" . $fileName . "</a></td>";
                    echo "<td><button type='submit' value='$fileName' class='deployFileName'>Deploy</button></td></tr>";
                }
            ?>
        </table>
        <p><a href="<?php echo "logs/" . $_SESSION['id'] . "/" . $_SESSION['id'] . "_workspaceDeployLog.txt" ?>">Download</a> workspace log file</p>
        </div>
        <?php else : ?>
            <p>You are not authorized to access this page. Please <a href="login.php">login</a>.</p>
        <?php endif; ?>
    </body>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script>
        $(function(){
            $('.deployFileName').on("click", function(){
                var fileName = $(this).val();
                $.ajax({
                    url : "/cgi-bin/workspaceDeploy.php",
                    data :  "fileName=" + fileName,
                    type : "GET",
                    dataType : "text",
                    success : function(data){
                        alert(data)},
                    fail : $("#status").text("Sorry! Unable to deploy. Please contact the administator.")
                });
            })
        });
    </script>
</html>

