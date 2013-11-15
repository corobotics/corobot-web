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
<?php include "include.php" ?>
<!-- 
    <div id="container">
      <div class="page">
      <div class="header">
        <a href="index.html" id="logo"></a>
        <ul>
          <li class="selected"><a href="home.html">Home</a></li>
          <li ><a href="index.html">Robot Location</a></li>-->
          <!--<li><a href="UploadModule/uploadcode.html">Upload Code</a></li>-->
<!--
          <li><a href="UploadModule/workspace.html">Workspace</a></li>
          <li><a href="status.html">Status</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
-->
      
    <div class="body">
      <h1>Welcome to the RIT Corobot server!</h1>

        <p>Our robots are ready and waiting on the third floor of the Golisano
        building to help you with tasks that you define.  These robots are
        already capable of navigating the building and reporting back to you,
        it's up to you (and your program) to tell them what to do.</p>
        
        <p>
        <ul>
        <li >See where the robots are right now <a href="index.php">here</a></li >
        <li ><a>Get the API to start writing your code (link)</a></li >
        <li >Log in to upload and deploy your code <a href="UploadModule/workspace.php">here</a></li >
        </ul>
        </p>
        <div >
          
    
        </div>
        <!--<ul class="blog">
          <li>
            <div>
              <a href="blog.html"><img src="GenericWeb/images/pastries.jpg" alt=""/></a>
              <p>Content 1.</p>
              <a href="blog.html">Click to read more</a>
            </div>
          </li>
          <li>
            <div>
              <a href="blog.html"><img src="GenericWeb/images/fruits.jpg" alt=""/></a>
               <p>Content 1.</p>
              <a href="blog.html">Click to read more</a>
            </div>
          </li>
          <li>
            <div>
              <a href="blog.html"><img src="GenericWeb/images/cosmetics.jpg" alt=""/></a>
               <p>Content 1.</p>
              <a href="blog.html">Click to read more</a>
            </div>
          </li>
        </ul>-->
      </div>
      <p id="text"></p>
    </div>

    <script type="application/dart" src="home"></script>
    <script src="https://dart.googlecode.com/svn/branches/bleeding_edge/dart/client/dart.js"></script>
  </body>
</html>