import 'dart:io';
import 'package:/options_file/options_file.dart';
import 'package:sqljocky/sqljocky.dart';
import 'package:sqljocky/utils.dart';
import 'data_access_layer.dart';
import 'static_file_handler.dart';
import 'connection_handler.dart';
import 'example.dart';


void main() {
  runServer(8080);
  dbConfig();
  
}

//Run Server function is created to create multiple instances 
//of server each with different basepath
runServer(int port) {
  HttpServer server = new HttpServer();
  //Multiple reuqest handler are added as shown below
  //The string passed in the path name which needs to accessed in order to 
  //execute function associated
  //with the handler
  server.addRequestHandler((req) => req.path =='/acceptInput',acceptInput);
  server.addRequestHandler((req) => req.path =='/acceptTest',acceptTest);
  WebSocketHandler webCon=new WebSocketHandler();
  webCon.onOpen = new ConnectionHandler("/portConnect").onOpen;
  server.addRequestHandler((req) => req.path == "/portConnect", webCon.onRequest);
  //Default handler is given just for the sake of making 
  //sure there is a default function handler
  server.defaultRequestHandler = new StaticFileHandler('/acceptInput').onRequest;
  server.listen('127.0.0.1', port);
  print('listening for connections on $port');
}

//The actual function which handles the accept input request
void acceptInput(HttpRequest request,HttpResponse response){
  print(request.connectionInfo.toString());
  print(request.queryParameters.toString());
  response.outputStream.write('Hello dude'.charCodes);
  response.outputStream.close();
}

void acceptTest(HttpRequest request,HttpResponse response){
  //The function is just used to test and manipulate the code
  //just an exploratory function
  print("Testfunction is getting called here");
  response.outputStream.write('Test Function'.charCodes);
  response.outputStream.close();
}


void dbConfig()
{
print("connection open");
var example = new Example();
// run the example
print("running example");
example.run().then((x) {
  // finally, close the connection
  example.pool.close();
});
}

