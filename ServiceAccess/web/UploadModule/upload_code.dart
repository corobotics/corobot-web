import 'dart:html';

class UploadCode {
  
}


void main(){
  InputElement uploadInput = query('#uploadFile');
  
  uploadInput.on.change.add((e) {
    // read file content as dataURL
    final files = uploadInput.files;
    if (files.length == 1) {
      final file = files[0];
      final reader = new FileReader();
      reader.on.load.add((e) {
        sendFile(reader.result);
      });
      reader.readAsText(file);
    }
  });
}

sendFile(dynamic data) {
  final req = new HttpRequest();
  req.on.readyStateChange.add((Event e) {
    if (req.readyState == HttpRequest.DONE &&
        (req.status == 200 || req.status == 0)) {
      window.alert("test successful");
    }
  });
  req.open("POST", "http://127.0.0.1:8080/upload");
  req.send(data);
  print(req.response);
}