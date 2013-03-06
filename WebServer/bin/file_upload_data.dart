library FileUploadData;
import 'sql/options_file/options_file.dart';
import 'sql/sqljocky/sqljocky.dart';
import 'dart:json';
class FileUploadData {
  var listOfPositions=new List<List>(); 
  ConnectionPool pool;
  FileUploadData(){
    OptionsFile options = new OptionsFile('connections.options');
    String user = options.getString('user');
    String password = options.getString('password');
    int port = options.getInt('port',3306);
    String db = options.getString('db');
    String host = options.getString('host','129.21.30.80');
    //Added to connection pool
    pool= new ConnectionPool(host: host, port: port, user: user, password: password, db: db);
  }
  
  Future InsertFileUpload(String username,String filename) {
    var completer = new Completer();
    pool.prepare("insert into UploadedFiles (Uname,Filename) values (?,?)").chain((query) {
      print("prepared query 1");
      var parameters = [
          [username,filename]
        ];
      return query.executeMulti(parameters);
    }).then((results) {
      completer.complete(null);
    });
    return completer.future;
  }
  
  Future getFileUploaded(String username) {
    var completer = new Completer();
    pool.prepare("Select idUpload,Uname,Filename from UploadedFiles where Uname=?").chain((query) {
      print("prepared query 1");
      var parameters = [
          [username]
        ];
      return query.executeMulti(parameters);
    }).then((results) {
      completer.complete(null);
    });
    return completer.future;
  }
}
