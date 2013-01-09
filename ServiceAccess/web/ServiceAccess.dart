import 'dart:html';
import 'socket_conn.dart';

void main() {
  SocketConn userClient=new SocketConn("ws://127.0.0.1:8080/portConnect");
  userClient.sendConnectionStatus("Client1","Handshake completed");
  /*
  HttpRequest req =new HttpRequest();
  req.on.readyStateChange.add((Event e) {
    if (req.readyState == HttpRequest.DONE &&
        (req.status == 200 || req.status == 0)) {
      onSuccess(req); // called when the POST successfully completes
    }
  });
  var url = "http://127.0.0.1:8080/acceptInput";
  req.open("POST", url); // Use POST http method to send data in the next call
  req.send("abc");
 */
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
