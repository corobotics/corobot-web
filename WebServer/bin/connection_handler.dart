library ConnectionHandler;
import 'dart:io';
class ConnectionHandler {
  Set<WebSocketConnection> webSocketConnections;

  ConnectionHandler(String basePath) : webSocketConnections = new Set<WebSocketConnection>() 
  
  {
    
  }

  // closures!
  onOpen(WebSocketConnection conn) {
    print('new ws conn');
    webSocketConnections.add(conn);

    conn.onClosed = (int status, String reason) {
      print('conn is closed');
      webSocketConnections.remove(conn);
    };

    conn.onMessage = (message) {
      print('new ws msg: $message');
      
      webSocketConnections.forEach((connection) {
        
        if (conn != connection) {
          print('queued msg to be sent');
          //queue(() => connection.send(message));
        }
      });
      //time('send to isolate', () => log.log(message));
    };
  }
}
