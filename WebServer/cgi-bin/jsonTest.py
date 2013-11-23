#!/usr/bin/python
import socket,json
print "Content-Type : application/json\n"
try:
    robotSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    robotSocket.connect (("129.21.30.80",61000))

    robotJsonData = robotSocket.recv (4096)
    if (robotJsonData):
        print json.dumps(robotJsonData)
    else:
        print "null"
    robotSocket.close()
except socket.error:
    print "null"
except Exception:
    print "null"

"""
sampleDict = {"a":1,"b":2}
print json.dumps (sampleDict)"""