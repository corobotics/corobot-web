#!/usr/bin/python
import socket,sys
print "Content-Type: text/plain\n"
#print "Browser test"
#print "Trying to connect to the server..."
# Type of message - <Type of message>DELIM<Total no of robots>DELIM<Robot No>DELIM<Robot name>DELIM<Robot status>
DELIM = ":"
ERROR_CODE = "E"
SUCCESS_CODE = "S"
HOST = "129.21.30.80"
PORT = 8081
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	conn.connect ((HOST,PORT))
except:
	print ERROR_CODE+DELIM
	sys.exit(1)
else:
	data = conn.recv (1024)
	msg = "BROWSER:check"
	conn.send (msg)
	data = conn.recv(1024)
	while True:
		if not data:
			break
		if data != "None":
			print SUCCESS_CODE+DELIM+data
		else:
			# No robots avail
			print ERROR_CODE+DELIM+"None"
			break
		conn.recv(1024)
	conn.close()

