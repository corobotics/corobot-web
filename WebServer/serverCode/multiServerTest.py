import socket,select,time,thread,json

sampleDict = {"a":1, "b":2}

# Function to print the current time and the data
def printWithTime(data):
	print ("%s--> %s" % (time.asctime(), data))

# Function to close the server.
def closeServer(serverSocket, browserSocket):
	"""Close all the sockets.
	serverSocket : server socket
	browserSocket : browser socket"""
	serverSocket.close()
	browserSocket.close()

# Start the server
def startServer():

	# Create the sockets
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	browserSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# Bind the sockets
	serverSocket.bind (("129.21.30.80",4000))
	browserSocket.bind (("129.21.30.80",4010))
	printWithTime ("Sockets binded successfully.")

	# Listen for incoming connections
	serverSocket.listen (10)
	browserSocket.listen(10)
	printWithTime ("Listening for incoming connections")
	
	return (serverSocket, browserSocket)

# Send JSON data to browser
def sendToBrowser (conn, ip, port, connectionType):
	try:
		printWithTime ("%s::%s:%d-Sending JSON data." % (connectionType, str(ip), port))
		jsonData = json.dumps (sampleDict)
		conn.send (jsonData)
		printWithTime ('JSON data sent. Closing connection.')
	except socket.error, msg:
		printWithTime ('Socket error with BROWSER! Closing connection!')
	finally:
		conn.close()


# Communicate with the robots
def communicate (conn, ip, port, connectionType):
	while True:
		try:
			data = conn.recv (1024)
			if not data:
				break
			printWithTime ("%s::%s:%d-data received : %s" % (connectionType,str(ip),port, data))
		except socket.error, (errNo,errMessage):
			printWithTime ("Error with %s::%s:%d. Error no : %d. Error Message : %s" % (connectionType, str(ip), port, errNo, errMessage))
			break
		except Exception as E:
			printWithTime ('Some exception! %s' % E)
	printWithTime ("Closing connection with %s :: %s:%d." % (connectionType,str(ip), port))
	conn.close()

		
# Main function
def main():
	""" Creating 3 lists for select() module.
		1. Input list
		2. Output list
		3. Error list"""

	serverSocket,browserSocket = startServer()

	# Create an input sockets list
	inputs = [serverSocket,browserSocket]

	# Create an output socket list
	outputs = []

	# Frequency to poll all channels in seconds
	timeout = 1

	try:
		while inputs:
			printWithTime ("\t---Waiting for next event to occur---")
			readable, writeable, exceptional = select.select (inputs, outputs, inputs)
			
			# Input channel
			for item in readable:
				# For server socket
				if item is serverSocket:
					conn, (ip,port) = serverSocket.accept()
					printWithTime (str (ip) + "::" + str(port) + "---SERVER connection.")
					# Communicate with the ROBOT socket.
					thread.start_new_thread (communicate, (conn,ip,port,"ROBOT", ))
				# For browser socket
				elif item is browserSocket:
					conn, (ip,port) = browserSocket.accept()
					printWithTime (str (ip) + "::" + str(port) + "---BROWSER connection.")
					# Send the JSON data to the incoming browser connection.
					thread.start_new_thread (sendToBrowser, (conn,ip,port,"BROWSER", ))
				else:
					printWithTime ("Unknown input connection")
					
			# Output channel
			for item in writeable:
				printWithTime ("%s available on output channel" %type(item))
				
			# Error channel
			for item in exceptional:
				printWithTime ("%s available on error channel" %type(item))

		
	except KeyboardInterrupt:
		printWithTime ("Keyboard interrupt!")

	except Exception as e:
		printWithTime ("Some exception-%s" % str(e))
	finally:
		closeServer(browserSocket, serverSocket)
		
if __name__ == "__main__":
	main()
	printWithTime ("Closing.")
