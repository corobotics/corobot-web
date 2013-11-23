#!/usr/bin/python
import subprocess, os, time
print ("Content-type : text/plain\n")
print ("Starting server...")
#ret_code = subprocess.call (["sudo","python", "/home/robotics/Desktop/gitWebServer/corobot-web/WebServer/serverCode/server.py"])

print os.system("sudo python /home/robotics/Desktop/gitWebServer/corobot-web/WebServer/serverCode/server.py")
time.sleep(3)
#os.system("^c")
"""if (ret_code == 0):
    print ("Server started succesfully.")
else:
    print ("Unable to start server.")"""