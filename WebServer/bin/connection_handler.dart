library ConnectionHandler;
/*
 * The library is used for handling socket communiucation from different client connections
 *
 * */
import 'dart:io';
import 'robot_data.dart';
import 'dart:json';
class ConnectionHandler {
  List positionCollection=new List<List>();
  Set<WebSocketConnection> webSocketConnections;

  ConnectionHandler(String basePath) : webSocketConnections = new Set<WebSocketConnection>()  
  {
    //For future use
  }

  onOpen(WebSocketConnection conn) {
    print('new ws conn');
    webSocketConnections.add(conn);
    conn.onClosed = (int status, String reason) {
      print('conn is closed');
      webSocketConnections.remove(conn);
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
}

