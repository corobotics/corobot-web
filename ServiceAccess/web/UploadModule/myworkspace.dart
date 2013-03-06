import 'dart:html';
import 'dart:json';
class Myworkspace {
  WebSocket socket;
  Object receivedData;
  Myworkspace(String url)
  {
    socket=new WebSocket(url);
    
    socket.on.open.add((e) {
      window.alert("Connected with the websocket");
      
    });
    
    socket.on.close.add((e){
      window.alert("Closed");
    });
    
    socket.on.message.add((MessageEvent e) {
      
      receivedData=e.data;
      
      final parsedList = JSON.parse(e.data);
      InputElement userInput = query('#uName');
      userInput.value=e.data.toString();
      var div = document.query('#tableContent');
      div.elements.clear();
      final s = new StringBuffer();
      s.add('<table class="table1">');
      s.add('<thead></thead>');
      s.add('<tr><th >Id</th><th>Robot Name</th><th>X Coordinate</th><th>Y Coordinate</th></tr>');
      for(final element in parsedList){
        window.alert(element);
        s.add('<tr><td>${element[0]}</td><td>${element[1]}</td><td>${element[2]}</td></tr>');
      }
      s.add('</table>');
      window.alert(s.toString());
      div.elements.add(new Element.html(s.toString()));

    });
  }
  _sendEncodedMessage(String encodedMessage) {
    if (socket != null && socket.readyState == WebSocket.OPEN) {
      socket.send(encodedMessage);
    } else {
      print('WebSocket not connected, message $encodedMessage not sent');
    }
  }
  
  send(String from, String message) {
    var encoded = JSON.stringify({'f': from, 'm': message});
    _sendEncodedMessage(encoded);
  }
}

String userName;
String password;
void main(){
  
  InputElement passwordInput = query('#pName');

  InputElement userInput = query('#uName');
  
  userInput.on.change.add((e){
    //window.alert(userInput.value);
    userName=userInput.value;
    
    
    
  });
  
  passwordInput.on.change.add((e){
    //window.alert(userInput.value);
    password=passwordInput.value;
    
  });
  
  Myworkspace userClient=new Myworkspace("ws://127.0.0.1:8080/getUploadedFile");
  ButtonElement btnSubmitInput = query('#login');
  btnSubmitInput.on.click.add((e){
    window.alert(userName);
    window.alert(password);
    final req = new HttpRequest();
  
   
    req.on.readyStateChange.add((Event e) {
      if (req.readyState == HttpRequest.DONE &&
          (req.status == 200 || req.status == 0)) {
        window.alert("test successful");
        window.alert(req.responseText);
      }
    });
    
    userClient.send(userName, "fileUpload");
    /*var fullString=new StringBuffer();
    fullString.add("http://129.21.30.80:8080/authenticate?");
    //fullString.add("http://127.0.0.1:8080/authenticate?");
    fullString.add("userName=");
    fullString.add(userName);
    fullString.add("&password=");
    fullString.add(password);
    //req.open("POST", "http://127.0.0.1:8080/upload?filename=$fileName");
    req.open("POST", fullString.toString());
    req.send("authenticate");*/
    //window.alert(req.responseText);
  });
  
}
