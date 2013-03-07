import 'dart:html';

class UploadCode {
  
}

String userName;

void main(){
  InputElement uploadInput = query('#uploadFile');

  InputElement userInput = query('#uName');
  
  userInput.on.change.add((e){
    //window.alert(userInput.value);
    userName=userInput.value;
    
  });

  uploadInput.on.change.add((e) {
    // read file content as dataURL
    final files = uploadInput.files;
    if (files.length == 1) {
      final file = files[0];
      String fileName=files[0].name;
      final reader = new FileReader();
      reader.on.load.add((e) {
        sendFile(reader.result,fileName,userName);
      });
      reader.readAsText(file);
    }
  });
}

sendFile(dynamic data,String fileName,String userName) {
  final req = new HttpRequest();
  req.on.readyStateChange.add((Event e) {
    if (req.readyState == HttpRequest.DONE &&
        (req.status == 200 || req.status == 0)) {
      window.alert("test successful");
    }
  });
  var fullString=new StringBuffer();
  fullString.add("http://127.0.0.1:8080/upload?");
  fullString.add("filename=");
  fullString.add(fileName);
  fullString.add("&user=");
  fullString.add(userName);
  //req.open("POST", "http://127.0.0.1:8080/upload?filename=$fileName");
  req.open("POST", fullString.toString());
  req.send(data);
  print(req.response);
}