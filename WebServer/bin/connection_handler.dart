library ConnectionHandler;
import 'dart:io';
import 'robot_data.dart';
class ConnectionHandler {
  Set<WebSocketConnection> webSocketConnections;

  ConnectionHandler(String basePath) : webSocketConnections = new Set<WebSocketConnection>() 
  
  {
    
  }

  // closures!
  onOpen(WebSocketConnection conn) {
    print('new ws conn');
    webSocketConnections.add(conn);

    /*conn.onClosed = (int status, String reason) {
      print('conn is closed');
      webSocketConnections.remove(conn);
    };*/

    for(int i=0;i<10;i++)
    {
      databaseUpdates();
    }
    //conn.send("test");
   
  }
  
  SendMessage(String broadCastMessage)
  {
    
  }
  
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

/*conn.onMessage = (message) {
  print('new ws msg: $message');
  
  webSocketConnections.forEach((connection) {
    
    if (conn != connection) {
      print('queued msg to be sent');
    }
  });
};*/
