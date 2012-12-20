import 'dart:html';
import 'dart:json';

class WebConnection {
  WebSocket webSocket;
  String url;

  WebConnection(this.url) {
    _init();
  }

  send(String from, String message) {
    //var encoded = JSON.stringify({'f': from, 'm': message});
    _sendEncodedMessage("abcd");
  }

  _receivedEncodedMessage(String encodedMessage) {
    print(encodedMessage);
    webSocket.send("tesds");
    /*Map message = JSON.parse(encodedMessage);
    if (message['f'] != null) {
    }*/
  }

  _sendEncodedMessage(String encodedMessage) {
    if (webSocket != null && webSocket.readyState == WebSocket.OPEN) {
      webSocket.send(encodedMessage);
      
    } else {
      print('WebSocket not connected, message $encodedMessage not sent');
    }
  }

  _init([int retrySeconds = 2]) {
    bool encounteredError = false;
    webSocket = new WebSocket(url);

    scheduleReconnect() {
      if (!encounteredError) {
        window.setTimeout(() => _init(retrySeconds*2), 1000*retrySeconds);
      }
      encounteredError = true;
    }

  
    webSocket.on.open.add((e) {
      print(e);
    });

    webSocket.on.close.add((e) => scheduleReconnect());
    webSocket.on.error.add((e) => scheduleReconnect());

    webSocket.on.message.add((MessageEvent e) {
      print('received message ${e.data}');
      _receivedEncodedMessage(e.data);
    });
  }

}


void main() {
  
  int k=0;
  WebConnection test= new WebConnection("ws://127.0.0.1:8080/portConnect");
  
  //while(h<15);
  if(k==1)
  {
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
  }
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
