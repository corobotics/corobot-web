library ConnectionHandler;
/*
 * The library is used for handling socket communiucation from different client connections
 *
 * */
import 'dart:io';
import 'robot_data.dart';
class ConnectionHandler {
  Set<WebSocketConnection> webSocketConnections;

  ConnectionHandler(String basePath) : webSocketConnections = new Set<WebSocketConnection>()  
  {
    //For future use
  }

  onOpen(WebSocketConnection conn) {
    print('new ws conn');
    webSocketConnections.add(conn);

    //Test Code for v alidating persistent communication
    for(int i=0;i<10;i++)
    {
      databaseUpdates();
    }
   
  }
  
  SendMessage(String broadCastMessage)
  {
    //Code to be written
  }
  
  //database update code
  void databaseUpdates()
  {
    print("connection open");

    var updatePosit=new RobotData();
    updatePosit.UpdateRobotPosition("testrobot", 24, 26).then((x){
      updatePosit.pool.close();
    });
    var getPosition=new RobotData();
    getPosition.GetAllRobotPosition().then((x){
      for (var row in getPosition.listOfPositions)
      {
        print(row);
      }
      getPosition.pool.close();
    });

    webSocketConnections.forEach((connection){
      connection.send("Robot position arrived");
      connection.send("Sending list");
    });

  }
}

