import 'dart:io';
void main() {
  var stream = new StringInputStream(stdin);  
}

void deployCode(String className)
{

  Process.run('javac',['-cp','.;classes.jar;',["HelloWorld.java"]]);
  Process.run('java',['-cp','.;classes.jar;','HelloWorld']).then((ProcessResult pr){
    print(pr.exitCode);
    print(pr.stdout);
    print(pr.stderr);
  });
}