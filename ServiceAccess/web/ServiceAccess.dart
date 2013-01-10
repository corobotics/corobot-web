import 'dart:html';
import 'socket_conn.dart';

void main() {
  SocketConn userClient=new SocketConn("ws://127.0.0.1:8080/portConnect");
  userClient.sendConnectionStatus("Client1","Handshake completed");
  
}

onSuccess(HttpRequest req) {
  
   window.alert(req.responseText.toString()); // print the received raw JSON text
}

void reverseText(Event event) {
  var text = query("#text").text;
  var buffer = new StringBuffer();
  for (int i = text.length - 1; i >= 0; i--) {
    buffer.add(text[i]);
  }
  query("#text").text = buffer.toString();
}
