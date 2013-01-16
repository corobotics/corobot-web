import 'dart:io';
import 'package:/options_file/options_file.dart';
import 'package:sqljocky/sqljocky.dart';
import 'package:sqljocky/utils.dart';
import 'static_file_handler.dart';
import 'connection_handler.dart';
import 'robot_data.dart';

ConnectionHandler connectedClient=new ConnectionHandler("/portConnect");
void main() {
  runServer(8080);
  
  deployCode();
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
  webCon.onOpen = connectedClient.onOpen;
  
  server.addRequestHandler((req) => req.path == "/portConnect", webCon.onRequest);
  server.addRequestHandler((req) => req.path == '/upload',UploadFile);
  //Default handler is given just for the sake of making 
  //sure there is a default function handler
  server.defaultRequestHandler = new StaticFileHandler('/acceptInput').onRequest;
  server.listen('127.0.0.1', port);
  print('listening for connections on $port');
}

void UploadFile(HttpRequest request, HttpResponse response) {
  print(request.inputStream.toString());
  response.outputStream.write('Upload File'.charCodes);
  response.outputStream.close();
}

  
//The actual function which handles the accept input request
void acceptInput(HttpRequest request,HttpResponse response){
  print(request.connectionInfo.toString());
  print(request.queryParameters);
  connectedClient.databaseUpdates(request.queryParameters["robotname"],int.parse(request.queryParameters["x"].toString()),int.parse(request.queryParameters["y"].toString()));
  response.outputStream.write('Hello dude'.charCodes);
  response.outputStream.close();
}

void acceptTest(HttpRequest request,HttpResponse response){

  print("Testfunction is getting called here");
  response.outputStream.write('Test Function'.charCodes);
  response.outputStream.close();
}


void databaseUpdates()
{
print("connection open");

var updatePosit=new RobotData();
updatePosit.UpdateRobotPosition("testrobot", 24, 26).then((x){
  updatePosit.pool.close();
});
var getPosition=new RobotData();
getPosition.GetAllRobotPosition().then((x){
  for (var row in getPosition.listOfPositions)
  {
    print(row);
  }
  getPosition.pool.close();
});

connectedClient.SendMessage("Test Robot Position Received");

}

void deployCode()
{
  Process.run('java',['-cp','.','HelloWorld']).then((ProcessResult pr){
    print(pr.exitCode);
    print(pr.stdout);
    print(pr.stderr);
  });
}

