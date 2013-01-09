library SocketConn;
import 'dart:html';
import 'dart:json';
class SocketConn {
  WebSocket socket;
  
  SocketConn(String url)
  {
    socket=new WebSocket(url);
    
    socket.on.open.add((e) {
      window.alert("Connected with the websocket");
    });
    
    socket.on.message.add((MessageEvent e) {
      print('${e.data}');
      
    });
  }
  
  sendConnectionStatus(String clientName, String message)
  {
    var encoded = JSON.stringify({'f': clientName, 'm': message});
    if (socket != null && socket.readyState == WebSocket.OPEN) {
      socket.send(encoded);
    } else {
      print("Error while sending message");
    }
  }
}
