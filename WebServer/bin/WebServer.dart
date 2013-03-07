import 'dart:io';
import 'package:options_file/options_file.dart';
import 'package:sqljocky/sqljocky.dart';
import 'package:sqljocky/utils.dart';
import 'static_file_handler.dart';
import 'connection_handler.dart';
import 'robot_data.dart';
List javafiles=new List();
List classes=new List();
ConnectionHandler connectedClient=new ConnectionHandler("/portConnect");
ConnectionHandler connectedFileUpload=new ConnectionHandler("/getUploadedFile");
void main() {
  runServer(8080);
  
  //deployCode();
}


//Run Server function is created to create multiple instances 
//of server each with different basepath
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
  
  WebSocketHandler webFileCon=new WebSocketHandler();
  webFileCon.onOpen = connectedFileUpload.onOpen;
  
  server.addRequestHandler((req) => req.path == "/portConnect", webCon.onRequest);
  server.addRequestHandler((req) => req.path == "/getUploadedFile", webFileCon.onRequest);
  
  server.addRequestHandler((req) => req.path == '/upload',UploadFile);
  
  server.addRequestHandler((req) => req.path == '/authenticate',authenticateUser);
  //Default handler is given just for the sake of making 
  //sure there is a default function handler
  server.defaultRequestHandler = new StaticFileHandler('/acceptInput').onRequest;
  server.listen('127.0.0.1', port);
  print('listening for connections on $port');
}

void authenticateUser(HttpRequest request, HttpResponse response) {
  print(request.queryParameters);
  
  String currentUser=request.queryParameters["userName"];
  print(request.queryParameters["userName"]);
  print(request.queryParameters["password"]);
  String s='CodeFolder/$currentUser';
  List options=new List();
  options.add('-a');
  options.add('-t');
  options.add(s);
  //var dir = new Directory('CodeFolder/$currentUser');
  
  
  
  

  Process.run('ls', options).then((ProcessResult results) {
    //print();
    
  //  response.outputStream.write(results.stdout.charCodes);
   // response.outputStream.close();
    //response.outputStream.writeString();
  });
  
  
  
}

void UploadFile(HttpRequest request, HttpResponse response) {
  print("handler called");
  print(request.queryParameters);
  print(request.queryParameters["user"]);
  String currentFilename=request.queryParameters["filename"].toString();
  String currentUser=request.queryParameters["user"].toString();
  print(request.inputStream.read(26));
  //response.outputStream.write('Upload File'.charCodes);
  //response.outputStream.close();
  _readBody(request,currentFilename,currentUser, (body,currentFilename,currentUser) {
    
    print(body);
    
    var dir = new Directory('CodeFolder/$currentUser');
    dir.createSync(recursive:true);
    var logFile = new File('CodeFolder/$currentUser/$currentFilename');
    
    connectedClient.workSpaceUpdate(currentUser, currentFilename);
    logFile.openSync(FileMode.APPEND);
    logFile.writeAsString(body);
    response.statusCode = HttpStatus.CREATED;
    response.contentLength = 0;
    response.outputStream.close();
  });
}

_readBody(HttpRequest request,String currentFilename,String currentUser, void handleContent(String body,String currentFilename,String currentUser)) {
  String contentString = ""; // request body byte data
  final completer = new Completer();
  final textFile = new StringInputStream(request.inputStream);
  textFile.onData = (){
    print("inside data");
    contentString = contentString.concat(textFile.read());
  };
  textFile.onClosed = () {
    completer.complete("");
  };
  textFile.onError = (Exception e) {
    print('exeption occured : ${e.toString()}');
  };
  
  // process the request and send a response
  completer.future.then((_){
    handleContent(contentString,currentFilename,currentUser);
  });
}
  
//The actual function which handles the accept input request
void acceptInput(HttpRequest request,HttpResponse response){
  print(request.connectionInfo.toString());
  print(request.queryParameters);
  print(request.queryParameters["robotname"]);
  print(request.queryParameters["x"]);
  print(request.queryParameters["y"]);
  connectedClient.databaseUpdates(request.queryParameters["robotname"],double.parse(request.queryParameters["x"].toString()),double.parse(request.queryParameters["y"].toString()));
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

/*void deployCode()
{
  Process.run('javac',['-cp','.;classes.jar;',["HelloWorld.java"]]);
  Process.run('java',['-cp','.;classes.jar;','HelloWorld']).then((ProcessResult pr){
    print(pr.exitCode);
    print(pr.stdout);
    print(pr.stderr);
  });
}*/

