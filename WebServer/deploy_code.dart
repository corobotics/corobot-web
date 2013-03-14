import 'dart:io';
import 'package:options_file/options_file.dart';
import 'package:sqljocky/sqljocky.dart';
import 'package:sqljocky/utils.dart';
List javafiles=new List();
List classes=new List();
void main() {
  deployCode(); 
}

void deployCode()
{

  classes.add('-cp');
  classes.add('.:classes.jar');
 
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

void executeCode()
{
  Process.start("javac",javafiles);
  Process.run('java', classes).then((ProcessResult pr){
    print(pr.exitCode);
    print(pr.stdout);
    print(pr.stderr);
  });
}
