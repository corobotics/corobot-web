#!/usr/bin/python
import socket
print ("Content-type : text/plain\n")
HOST = "129.21.30.80"
PORT = 56000
WAY_POINT = "ehall0"
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect ((HOST,PORT))
    client.sendall (WAY_POINT)
    while True:
        data = client.recv(1024)
        if not data:
            break
        print data
except socket.error, (errNo, errMessage):
    print ("Error while starting server. Error code : %d. Error message : %s. Terminating!!!" % (errNo, errMessage))
finally:
    client.close()