library ConnectionHandler;
import 'dart:io';
import 'dart:isolate';
class ConnectionHandler {
  Set<WebSocketConnection> webSocketConnections;

  ConnectionHandler(String basePath) : webSocketConnections = new Set<WebSocketConnection>() 
  
  {
    
  }

  // closures!
  onOpen(WebSocketConnection conn) {
    print('new ws conn');
    print(conn.toString());
    webSocketConnections.add(conn);
    conn.send("tee");
    conn.onClosed = (int status, String reason) {
      print('conn is closed');
      webSocketConnections.remove(conn);
    };
  
   
    conn.onMessage = (message) {
      print('new ws msg: $message');
      conn.send("mila message");
      /*webSocketConnections.forEach((connection) {
        
        if (conn != connection) {
          
          //queue(() => connection.send(message));
        }
      });*/
      //time('send to isolate', () => log.log(message));
    };
  }
}
