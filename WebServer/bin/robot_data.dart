library RobotData;
/*
 * The library is used for fetching information about the robot position.
 * 
 */
import 'sql/options_file/options_file.dart';
import 'sql/sqljocky/sqljocky.dart';
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
    String host = options.getString('host','129.21.30.80');
    //Added to connection pool
    pool= new ConnectionPool(host: host, port: port, user: user, password: password, db: db);
 
  }
  
  //Sends the later robot position to table as given by the robot
  Future UpdateRobotPosition(String robotname,double xcoordinate,double ycoordinate) {
    var completer = new Completer();
    
    pool.prepare("Update robotposition set isCurrentPosition='0' where robotname='$robotname'").then((query){
     return query.execute().then((x){
       pool.prepare("insert into robotposition (robotname,xcoordinate,ycoordinate,isCurrentPosition) values (?,?,?,1)").chain((query) {
         var parameters = [
                           [robotname,xcoordinate,ycoordinate]
                           ];
         return query.executeMulti(parameters);
       }).then((results) {
         completer.complete(null);
       });
       return completer.future;   
     }); 
     return completer.future;
    });
  }
  
  //Gets all the position of robots from the table in the database
  Future GetAllRobotPosition()
  {
    var completer = new Completer();
    pool.query("SELECT idrobotPosition,robotname,ycoordinate,xcoordinate FROM robotPosition where isCurrentPosition='1'").then((x){
      for (var row in x) {   
        List parsedList = row;
        listOfPositions.add(parsedList);
       }
      completer.complete(null);
    });
    return completer.future;
  }
}
