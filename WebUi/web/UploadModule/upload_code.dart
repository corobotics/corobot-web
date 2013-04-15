import 'dart:html';

class UploadCode {
  String userName;
  String password;
  
  UploadCode(){
    InputElement uploadInput = query('#uploadFile');

    InputElement userInput = query('#uName');
    InputElement passWordInput = query('#passWord');
    
    userInput.on.change.add((e){
      //window.alert(userInput.value);
      userName=userInput.value;
      
    });
    
    passWordInput.on.change.add((e){
      //window.alert(userInput.value);
      password=passWordInput.value;
      
    });

    uploadInput.on.change.add((e) {
      // read file content as dataURL
      final files = uploadInput.files;
      if (files.length == 1) {
        final file = files[0];
        String fileName=files[0].name;
        final reader = new FileReader();
        reader.on.load.add((e) {
          sendFile(reader.result,fileName,userName,password);
        });
        reader.readAsText(file);
      }
    });
  }
}


String userName;
String password;
void main(){
  InputElement uploadInput = query('#uploadFile');

  InputElement userInput = query('#uName');
  InputElement passWordInput = query('#passWord');
  
  userInput.on.change.add((e){
    //window.alert(userInput.value);
    userName=userInput.value;
    
  });
  
  passWordInput.on.change.add((e){
    //window.alert(userInput.value);
    password=passWordInput.value;
    
  });

  uploadInput.on.change.add((e) {
    // read file content as dataURL
    final files = uploadInput.files;
    if (files.length == 1) {
      final file = files[0];
      String fileName=files[0].name;
      final reader = new FileReader();
      reader.on.load.add((e) {
        sendFile(reader.result,fileName,userName,password);
      });
      reader.readAsText(file);
    }
  });
}

sendFile(dynamic data,String fileName,String userName,String password) {
  final req = new HttpRequest();
  req.on.readyStateChange.add((Event e) {
    if (req.readyState == HttpRequest.DONE &&
        (req.status == 200 || req.status == 0)) {
     // window.alert("test successful");
    }
  });
  var fullString=new StringBuffer();
  fullString.add("http://129.21.30.80:8080/upload?");
  fullString.add("filename=");
  fullString.add(fileName);
  fullString.add("&user=");
  fullString.add(userName);
  fullString.add("&password=");
  fullString.add(password);
  //req.open("POST", "http://127.0.0.1:8080/upload?filename=$fileName");
  req.open("POST", fullString.toString());
  req.send(data);
  print(req.response);
}