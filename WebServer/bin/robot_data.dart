library RobotData;
import 'sql/options_file/options_file.dart';
import 'sql/sqljocky/sqljocky.dart';
import 'robot_data_structure.dart';
import 'dart:json';

//The connection with database is established here.
//The updates given by robot are pushed to database here
class RobotData {
  var listOfPositions=new List<List>(); 
  ConnectionPool pool;
  RobotData()
  {
    //Connection string is created
    OptionsFile options = new OptionsFile('connections.options');
    String user = options.getString('user');
    String password = options.getString('password');
    int port = options.getInt('port',3306);
    String db = options.getString('db');
    String host = options.getString('host','localhost');
    //Added to connection pool
    pool= new ConnectionPool(host: host, port: port, user: user, password: password, db: db);
 
  }
  
  //Sends the later robot position to table as given by the robot
  Future UpdateRobotPosition(String robotname,int xcoordinate,int ycoordinate) {
    var completer = new Completer();
    pool.prepare("insert into robotposition (robotname,xcoordinate,ycoordinate) values (?,?,?)").chain((query) {
      print("prepared query 1");
      var parameters = [
          [robotname,xcoordinate,ycoordinate]
        ];
      return query.executeMulti(parameters);
    }).then((results) {
      completer.complete(null);
    });
    return completer.future;
  }
  
  //Gets all the position of robots from the table in the database
  Future GetAllRobotPosition()
  {
    var completer = new Completer();
    pool.query("SELECT idrobotPosition,robotname,ycoordinate,xcoordinate FROM robotPosition").then((x){
      print("got results");
      for (var row in x) {   
        List parsedList = row;
        listOfPositions.add(parsedList);
       }
      completer.complete(null);
    });
    return completer.future;
  }
}
