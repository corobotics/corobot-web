import 'dart:html';

class Myworkspace {
  
}

String userName;
String password;
void main(){
  InputElement passwordInput = query('#pName');

  InputElement userInput = query('#uName');
  
  userInput.on.change.add((e){
    //window.alert(userInput.value);
    userName=userInput.value;
    
    
    
  });
  
  passwordInput.on.change.add((e){
    //window.alert(userInput.value);
    password=passwordInput.value;
    
  });
  
  ButtonElement btnSubmitInput = query('#login');
  btnSubmitInput.on.click.add((e){
    window.alert(userName);
    window.alert(password);
    final req = new HttpRequest();
  
    req.on.loadEnd.add((e){
      if (req.readyState == HttpRequest.LOADING &&
          (req.status == 200 || req.status == 0)) {
        window.alert(req.responseText);
      }
    });
    req.on.readyStateChange.add((Event e) {
      if (req.readyState == HttpRequest.DONE &&
          (req.status == 200 || req.status == 0)) {
        window.alert("test successful");
        window.alert(req.responseText);
      }
    });
    var fullString=new StringBuffer();
    fullString.add("http://129.21.30.80:8080/authenticate?");
    //fullString.add("http://127.0.0.1:8080/authenticate?");
    fullString.add("userName=");
    fullString.add(userName);
    fullString.add("&password=");
    fullString.add(password);
    //req.open("POST", "http://127.0.0.1:8080/upload?filename=$fileName");
    req.open("POST", fullString.toString());
    req.send("authenticate");
    //window.alert(req.responseText);
  });
  
}