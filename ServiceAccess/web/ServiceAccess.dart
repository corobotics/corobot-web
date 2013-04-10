import 'dart:html';
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
     
      final parsedList = JSON.parse(e.data);
      window.alert(e.data.toString());
      var div = document.query('#tableContent');
      div.elements.clear();
      final s = new StringBuffer();
      s.add('<table class="table1">');
      s.add('<thead></thead>');
      s.add('<tr><th >Id</th><th>Robot Name</th><th>X Coordinate</th><th>Y Coordinate</th></tr>');
      for(final element in parsedList){
        s.add('<tr><td>${element[0]}</td><td>${element[1]}</td><td>${element[3]}</td><td>${element[2]}</td></tr>');
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
  SocketConn userClient=new SocketConn("ws://129.21.30.80:8080/portConnect"); 
  ButtonElement getCurrentRobotLocation = query('#getData');
  getCurrentRobotLocation.on.click.add((e){
   // userClient.send('$userName|$filelist|$numfiles',"deploy");
  });
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


