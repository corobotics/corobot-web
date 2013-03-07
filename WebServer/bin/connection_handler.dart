library ConnectionHandler;
/*
 * The library is used for handling socket communiucation from different client connections
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
    print('new ws conn');

    webSocketConnections.add(conn);
    conn.onClosed = (int status, String reason) {
      print('conn is closed');
      //webSocketConnections.remove(conn);
    };


   conn.onMessage=void Message(m){
     Map parsedMap=JSON.parse(m);
     print(parsedMap);
     if(parsedMap["m"]=="fileUpload")
     {
       var getFileUploaded=new FileUploadData();
       getFileUploaded.getFileUploaded(parsedMap["f"]).then((x){
         for (var row in getFileUploaded.listOfPositions)
         { 
           fileCollection.add(row); 
           
         }
         var encoded=JSON.stringify(fileCollection);
         print(fileCollection);
         conn.send(encoded);
         getFileUploaded.pool.close();
         positionCollection.clear();
       });
     }else if(parsedMap["m"]=="deploy"){
       
     }
   };
  }
  
  SendMessage(String broadCastMessage)
  {
    //Code to be written
  }
  
  
  //database update code
  databaseUpdates(String robotname,double xcoordinate,double ycoordinate)
  {
    //print("connection open");

    var updatePosit=new RobotData();
    updatePosit.UpdateRobotPosition(robotname, xcoordinate, ycoordinate).then((x){
      var getPosition=new RobotData();
      getPosition.GetAllRobotPosition().then((x){
        for (var row in getPosition.listOfPositions)
        { 
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
  
  workSpaceUpdate(String username,String filename)
  {
    var updateFileList=new FileUploadData();
    updateFileList.InsertFileUpload(username, filename).then((x){
      /*var getFileUploaded=new FileUploadData();
      getFileUploaded.getFileUploaded(username).then((x){
        for (var row in getFileUploaded.listOfPositions)
        { 
          fileCollection.add(row); 
          
        }
        var encoded=JSON.stringify(positionCollection);
        webSocketConnections.forEach((connect){
          if(connection.toString()==connect.toString())
          {
            connect.send(encoded);
          }
          
        });
        getFileUploaded.pool.close();
        positionCollection.clear();
      });*/
      updateFileList.pool.close();
    });
  }
  
  getFileUpload(String username){
    var getFileUploaded=new FileUploadData();
    getFileUploaded.getFileUploaded(username).then((x){
      for (var row in getFileUploaded.listOfPositions)
      { 
        fileCollection.add(row); 
        
      }
      var encoded=JSON.stringify(positionCollection);
      print(encoded);
      webSocketConnections.forEach((connect){
        /*if(connection.toString()==connect.toString())
        {
          connect.send(encoded);
        }*/
        
      });
      getFileUploaded.pool.close();
      positionCollection.clear();
    });
  }
  
  void deployCode()
  {

    classes.add('-cp');
    classes.add('.:classes.jar');
    
    javafiles.add('-cp');
    javafiles.add('.:classes.jar');
    var stream = new StringInputStream(stdin);
    stream.onLine = () {
      var str = stream.readLine().trim();
      if(str == 'EXIT') 
      {
        executeCode();
      }
      else
      {
        String abc= "$str.java";
        print(abc);
        javafiles.add(abc);
        classes.add(str);
      }
    };

  }

  void executeCode()
  {
    Process.start("javac",javafiles);
    Process.run('java', classes).then((ProcessResult pr){
      print(pr.exitCode);
      print(pr.stdout);
      print(pr.stderr);
    });
  }
}

