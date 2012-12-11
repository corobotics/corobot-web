import 'dart:io';
import 'package:/options_file/options_file.dart';
import 'package:sqljocky/sqljocky.dart';
import 'package:sqljocky/utils.dart';
import 'data_access_layer.dart';
import 'static_file_handler.dart';
import 'connection_handler.dart';
void main() {
  dbConfig();
  runServer(8080);
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
OptionsFile options = new OptionsFile('connection.options');
String user = options.getString('user');
String password = options.getString('password');
int port = options.getInt('port',3306);
String db = options.getString('db');
String host = options.getString('host','localhost');
print(password);
var pool = new ConnectionPool(host: host, port: port, user: user, password: password, db: db);
print("connection open");
pool.query('select p.id, p.name, p.age, t.name, t.species '
    'from people p '
'left join pets t on t.owner_id = p.id').then(onSuccess);
}

onSuccess(result)
{
  for (var row in result) {
    if (row[3] == null) {
      print("ID: ${row[0]}, Name: ${row[1]}, Age: ${row[2]}, No Pets");
    } else {
      print("ID: ${row[0]}, Name: ${row[1]}, Age: ${row[2]}, Pet Name: ${row[3]},     Pet Species ${row[4]}");
    }
  }
}