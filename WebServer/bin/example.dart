library Example;
import 'sql/sqljocky/sqljocky.dart';
import 'sql/sqljocky/utils.dart';
import 'sql/options_file/options_file.dart';
class Example {
  ConnectionPool pool;
  Example()
  {
    OptionsFile options = new OptionsFile('connections.options');
    String user = options.getString('user');
    String password = options.getString('password');
    int port = options.getInt('port',3306);
    String db = options.getString('db');
    String host = options.getString('host','localhost');
    pool= new ConnectionPool(host: host, port: port, user: user, password: password, db: db);
  }
  
  Future run() {
    var completer = new Completer();
    // drop the tables if they already exist
    dropTables().chain((x) {
      print("dropped tables");
      // then recreate the tables
      return createTables();
    }).chain((x) {
      print("created tables");
      // add some data
      return addData();
    }).chain((x) {
      // and read it back out
      return readData();
    }).then((x) {
      completer.complete(null);
    });
    return completer.future;
  }

  Future dropTables() {
    print("dropping tables");
    var dropper = new TableDropper(pool, ['pets', 'people']);
    return dropper.dropTables();
  }
  
  Future createTables() {
    print("creating tables");
    var querier = new QueryRunner(pool, ['create table people (id integer not null auto_increment, '
                                        'name varchar(255), '
                                        'age integer, '
                                        'primary key (id))',
                                        
                                        'create table pets (id integer not null auto_increment, '
                                        'name varchar(255), '
                                        'species varchar(255), '
                                        'owner_id integer, '
                                        'primary key (id),'
                                        'foreign key (owner_id) references people (id))'
                                        ]);
    print("executing queries");
    return querier.executeQueries();
  }
  
  Future addData() {
    var completer = new Completer();
    pool.prepare("insert into people (name, age) values (?, ?)").chain((query) {
      print("prepared query 1");
      var parameters = [
          ["Dave", 15],
          ["John", 16],
          ["Mavis", 93]
        ];
      return query.executeMulti(parameters);
    }).chain((results) {
      print("executed query 1");
      return pool.prepare("insert into pets (name, species, owner_id) values (?, ?, ?)");
    }).chain((query) {
      print("prepared query 2");
      var parameters = [
          ["Rover", "Dog", 1],
          ["Daisy", "Cow", 2],
          ["Spot", "Dog", 2]];
      return query.executeMulti(parameters);
    }).then((results) {
      print("executed query 2");
      completer.complete(null);
    });
    return completer.future;
  }
  
  Future readData() {
    var completer = new Completer();
    print("querying");
    pool.query('select p.id, p.name, p.age, t.name, t.species '
        'from people p '
        'left join pets t on t.owner_id = p.id').then((result) {
      print("got results");
      for (var row in result) {
        if (row[3] == null) {
          print("ID: ${row[0]}, Name: ${row[1]}, Age: ${row[2]}, No Pets");
        } else {
          print("ID: ${row[0]}, Name: ${row[1]}, Age: ${row[2]}, Pet Name: ${row[3]}, Pet Species ${row[4]}");
        }
      }
      completer.complete(null);
    });
    return completer.future;
  }
}