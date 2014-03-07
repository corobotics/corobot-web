#!/usr/bin/python
import os
path = "/home/robotics/Desktop/gitWebServer/corobot-web/WebServer/serverCode/"
filename = "server.py"

# Function to check if a program is running.
def checkProgram():
    #print (((os.popen("ps -ef | grep \"python.*%s\"" % filename)).read()).strip())
    return int(((os.popen("ps -ef | grep -c \"python.*%s\"" % filename)).read()).strip())

print ("Content-type : text/plain\n")
try:
    # Check if the server program is running.
    result = checkProgram()
    
    # NOTE : result will be >= 2 while executing this program manually at the terminal
    # result >= 3 when executed remotely. 
    if (result >= 3):
        print ("Server is already running!")

    # Start the server
    else:
        os.chdir(path)
        os.system("python %s &" % (path + filename))
        print ("Server has been started.")  
      
except Exception:
    print ("Sorry, unable to start the server program. Please contact the administrator.")
