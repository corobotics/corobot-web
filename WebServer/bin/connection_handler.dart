library ConnectionHandler;
/*
 * The library is used for handling socket communication from different client connections
 *
 * */
import 'dart:io';
import 'robot_data.dart';
import 'file_upload_data.dart';
import 'dart:json';
List javafiles=new List();
List classes=new List();
class ConnectionHandler {
  List positionCollection=new List<List>();
  List fileCollection=new List<List>();
  Set<WebSocketConnection> webSocketConnections;
  Map<String,WebSocketConnection> fileUploadSocketConnections;
  ConnectionHandler(String basePath) : webSocketConnections = new Set<WebSocketConnection>()  
  {
    //For future use
  }

  onOpen(WebSocketConnection conn) {
    webSocketConnections.add(conn);
    conn.onClosed = (int status, String reason) {
      webSocketConnections.remove(conn);
    };


   conn.onMessage=void Message(m){
     Map parsedMap=JSON.parse(m);
     fileCollection.clear();
     if(parsedMap["m"]=="fileUpload")
     {
       List<String> userDetails=parsedMap["f"].split("|");
       var getFileUploaded=new FileUploadData();
       getFileUploaded.authenticateUser(userDetails[0],userDetails[1]).then((x){
         if(getFileUploaded.isAuthenticated){
           getFileUploaded.getFileUploaded(userDetails[0]).then((x){
             for (var row in getFileUploaded.listOfPositions){ 
               fileCollection.add(row); 
             }
             var encoded=JSON.stringify(fileCollection);
             conn.send(encoded);
             getFileUploaded.pool.close();
             positionCollection.clear();
           });
         }
       });  
     }
     else if(parsedMap["m"]=="deploy"){
       List<String> content=parsedMap["f"].split('|');
       deployCode(conn,content[0],content[1],int.parse(content[2]));
     }
   };
  }
  
  SendMessage(String broadCastMessage){
    //Code to be written
  }
  
  
  //database update code
  databaseUpdates(String robotname,double xcoordinate,double ycoordinate){

    var updatePosit=new RobotData();
    updatePosit.UpdateRobotPosition(robotname, xcoordinate, ycoordinate).then((x){
      var getPosition=new RobotData();
      getPosition.GetAllRobotPosition().then((x){
        for (var row in getPosition.listOfPositions){ 
          positionCollection.add(row); 
          
        }
        var encoded=JSON.stringify(positionCollection);
        webSocketConnections.forEach((connection){
          connection.send(encoded);
        });
        getPosition.pool.close();
        positionCollection.clear();
      });
      updatePosit.pool.close();
    }); 
  }
  
  //Currently not being used, just a sample demonstration code of POC
  workSpaceUpdate(String username,String password,String filename,String body)
  {
    var getFileUploaded=new FileUploadData();
    getFileUploaded.authenticateUser(username,password).then((x){
      if(getFileUploaded.isAuthenticated){
        var updateFileList=new FileUploadData();
        updateFileList.InsertFileUpload(username, filename).then((x){
          updateFileList.pool.close();
          var dir = new Directory('CodeFolder/$username');
          dir.createSync(recursive:true);
          var logFile = new File('CodeFolder/$username/$filename');
          logFile.openSync(FileMode.APPEND);
          logFile.writeAsString(body);
        });
      }
    });
  }
  
  //Currently not being used, just a sample demonstration code of POC
  getFileUpload(String username){
    var getFileUploaded=new FileUploadData();
    fileCollection.clear();
    getFileUploaded.getFileUploaded(username).then((x){
      for (var row in getFileUploaded.listOfPositions){ 
        fileCollection.add(row); 
      }
      var encoded=JSON.stringify(positionCollection);
      print(encoded);
      webSocketConnections.forEach((connect){
      });
      getFileUploaded.pool.close();
      positionCollection.clear();
    });
  }
  
  //Currently has the issue of copying the classes.jar to each user folder
  void deployCode(WebSocketConnection conn,String userName,String files,int count){
    classes.add('-cp');
    classes.add('CodeFolder/classes.jar:CodeFolder/$userName');
    int index=0;
    javafiles.add('-cp');
    javafiles.add('CodeFolder/classes.jar');
    List<String> fileCollection=files.split(" ");
    fileCollection.forEach((x){
      String abc= "CodeFolder/$userName/$x.java";
      String def= "$x";
      print(def);
      print(abc);
      javafiles.add(abc);
      classes.add(def);
      index++;
    });
    do{
      executeCode(conn);
    }while(index<count);
  }

  //Executes the java code and sends the stdout messages to the user
  void executeCode(WebSocketConnection conn){
    //Untested code for compilation has some issues to asynchronous call
    
    //Process.start("javac",javafiles);
    print(classes);
    
    //Currently untested code but will be rectified to make it work.
    
    Process.run("javac",javafiles).then((ProcessResult pr){
      Process.run('java', classes).then((ProcessResult pr){
        String a=pr.stdout;
        String b=pr.stderr;
        //conn.send(pr.exitCode);
        conn.send(a);
        conn.send(b);
        print(pr.exitCode);
        print(pr.stdout);
        print(pr.stderr);
        
      });    
    });
  }
}

