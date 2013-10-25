#!/usr/bin/python

import socket
print "Content-Type: text/plain\n"
host = "129.21.30.80"
port = 8080
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect ((host,port))
data = conn.recv (1024)
msg = "browser - check"
conn.send (msg)
conn.close()
print "Data received : " + data
