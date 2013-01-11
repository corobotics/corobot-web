import 'dart:html';
import 'socket_conn.dart';
import 'dart:json';

class SocketConn {
  WebSocket socket;
  Object receivedData;
  SocketConn(String url)
  {
    socket=new WebSocket(url);
    
    socket.on.open.add((e) {
      window.alert("Connected with the websocket");
    });
    
    socket.on.message.add((MessageEvent e) {
      receivedData=e.data;
      //Map message = JSON.parse(e.data);
      /*
       * message.forEach((x){
        query("#idData").append(x);
      });*/
     
      //JSON.parse(e.data);
      /*final s = new StringBuffer();
      TableElement grid=query("#idData");
      final parsedList = JSON.parse(e.data)/*.fore*/;
      s.add('<table>');
      s.add('<thead></thead>');
      for(final abcd in parsedList){
        s.add('<tr><td>${abcd}</td></tr>');
      }
      s.add('</table>');
      
      Element tabledata=new Element.html(s.toString()) as TableElement;
      query("newTable").innerHTML=s;
      */
      
      final parsedList = JSON.parse(e.data);
      var div = document.query('#tableContent');
      final s = new StringBuffer();

      s.add('<table>');
      s.add('<thead></thead>');
      s.add('<tr><td>Robot Name</td><td>X Coordinate</td><td>Y Coordinate</td></tr>');
      for(final element in parsedList){
        s.add('<tr><td>${element[1]}</td><td>${element[2]}</td><td>${element[3]}</td></tr>');
      }
      s.add('</table>');
      div.elements.add(new Element.html(s.toString()));

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


void main() {
  SocketConn userClient=new SocketConn("ws://127.0.0.1:8080/portConnect"); 
  
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


