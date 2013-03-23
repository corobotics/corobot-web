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
}

//Unused code need to be removed after testing.
void deployCode()
{
  classes.add('-cp');
  classes.add('.');
  javafiles.add('-cp');
  javafiles.add('.:classes.jar');
  var stream = new StringInputStream(stdin);
  stream.onLine = () {
    var str = stream.readLine().trim();
    if(str == 'EXIT') 
    {
      executeCode();
    }
    else
    {
    String abc= "$str.java";
    print(abc);
    javafiles.add(abc);
    classes.add(str);
    }
  };
}

//old code for executing java process from dartvm.
void executeCode()
{
  Process.start("javac",javafiles);
  Process.run('java', classes).then((ProcessResult pr){
    print(pr.exitCode);
    print(pr.stdout);
    print(pr.stderr);
  });
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
  server.listen('129.21.30.80', port);
  print('listening for connections on $port');
}

//temp authentication which needs to be removed.
void authenticateUser(HttpRequest request, HttpResponse response) {
  String currentUser=request.queryParameters["userName"];
  print(request.queryParameters["userName"]);
  print(request.queryParameters["password"]);
  String s='CodeFolder/$currentUser';
  List options=new List();
  options.add('-a');
  options.add('-t');
  options.add(s);
  Process.run('ls', options).then((ProcessResult results) {
  });
}

void UploadFile(HttpRequest request, HttpResponse response) {
  String currentFilename=request.queryParameters["filename"].toString();
  String currentUser=request.queryParameters["user"].toString();
  String currentUserPassword=request.queryParameters["password"].toString(); 

  //The function below is a delegate for reading the entire file and its 
  //content
    _readBody(request,currentFilename,currentUserPassword,currentUser, (body,currentFilename,currentUserPassword,currentUser) {
    connectedClient.workSpaceUpdate(currentUser,currentUserPassword, currentFilename,body);
    response.statusCode = HttpStatus.CREATED;
    response.contentLength = 0;
    response.outputStream.close();
  });
}

//Basic function to read and traverse the file contents.
_readBody(HttpRequest request,String currentFilename,String currentUserPassword,String currentUser, void handleContent(String body,String currentFilename,String currentUserPassword,String currentUser)) {
  String contentString = ""; // request body byte data
  final completer = new Completer();
  final textFile = new StringInputStream(request.inputStream);
  textFile.onData = (){
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
    handleContent(contentString,currentFilename,currentUserPassword,currentUser);
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


//Basic handler testing function will be displayed for production release.
void acceptTest(HttpRequest request,HttpResponse response){

  print("Testfunction is getting called here");
  response.outputStream.write('Test Function'.charCodes);
  response.outputStream.close();
}

//Old code used for testing needs to be removed.
void databaseUpdates(){
  var updatePosit=new RobotData();
  updatePosit.UpdateRobotPosition("testrobot", 24.00, 26.00).then((x){
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

