library RobotData;
import 'sql/options_file/options_file.dart';
import 'sql/sqljocky/sqljocky.dart';
import 'robot_data_structure.dart';
import 'dart:json';
class RobotData {
  var listOfPositions=new List<List>(); 
  ConnectionPool pool;
  RobotData()
  {
    OptionsFile options = new OptionsFile('connections.options');
    String user = options.getString('user');
    String password = options.getString('password');
    int port = options.getInt('port',3306);
    String db = options.getString('db');
    String host = options.getString('host','localhost');
    pool= new ConnectionPool(host: host, port: port, user: user, password: password, db: db);
 
  }
  
  Future UpdateRobotPosition(String robotname,int xcoordinate,int ycoordinate) {
    var completer = new Completer();
    pool.prepare("insert into robotposition (robotname,xcoordinate,ycoordinate) values (?,?,?)").chain((query) {
      print("prepared query 1");
      var parameters = [
          [robotname,xcoordinate,ycoordinate]
        ];
      return query.executeMulti(parameters);
    }).then((results) {
      //print("query executed");
      //print(results);
      completer.complete(null);
    });
    return completer.future;
  }
  
  Future GetAllRobotPosition()
  {
    
    var completer = new Completer();
    pool.query("SELECT idrobotPosition,robotname,ycoordinate,xcoordinate FROM robotPosition").then((x){
      print("got results");
      for (var row in x) {   
        
        List parsedList = row;
        listOfPositions.add(parsedList);
        //print(listOfPositions[0][1]);
        
        /*print(parsedList[0]);
        print(parsedList[1]);*/ 
        //print("idrobotPosition: ${row[0]}, robotname: ${row[1]}, ycoordinate: ${row[2]}, xcoordinate: ${row[3]}");
      }
      completer.complete(null);
    });
    return completer.future;
  }
}
