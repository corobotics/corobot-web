import socket,sys,thread,time, select, json

# Function to initialize with default values
def init (WELCOME_MSG="", HOST="", SERVER_PORT=0, BROWSER_PORT=0, BUFFER_SIZE=0, MAX_NO_OF_CONNECTIONS=0,
		ROBOTS_INFO_DICT={}, DELIM="",SERVER_STATUS_FILE=""):
	"""
	Includes variables for the default communication setup.
	If any of the parameters are not defined, use the mentioned default 
	ones."""

	if WELCOME_MSG == "" :
		WELCOME_MSG = "Welcome to corobotics server."
	if HOST == "":
		HOST = "129.21.30.80"
	if SERVER_PORT == 0:
		SERVER_PORT = 51000
	if BROWSER_PORT == 0:
		BROWSER_PORT = 61000
	if BUFFER_SIZE == 0:
		BUFFER_SIZE = 4096
	if MAX_NO_OF_CONNECTIONS == 0:
		MAX_NO_OF_CONNECTIONS = 10
	if ROBOTS_INFO_DICT == {}:
		ROBOTS_INFO_DICT = {}
	if DELIM == "":
		DELIM = ":"
	if SERVER_STATUS_FILE == "":
		SERVER_STATUS_FILE = "serverStatusLog.txt"
	
	globals()["WELCOME_MSG"] = WELCOME_MSG
	globals()["HOST"] = HOST
	globals()["SERVER_PORT"] = SERVER_PORT
	globals()["BROWSER_PORT"] = BROWSER_PORT
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	globals()["MAX_NO_OF_CONNECTIONS"] = MAX_NO_OF_CONNECTIONS
	globals()["ROBOTS_INFO_DICT"] = ROBOTS_INFO_DICT
	globals()["DELIM"] = DELIM
	globals()["SERVER_STATUS_FILE"] = SERVER_STATUS_FILE

	# Open server status file in append + reading mode
	global statusFileHandler
	statusFileHandler = open ("SERVER_STATUS_FILE","a+")

	# DEBUG 
	"""printWithTime ("Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\n\
		SERVER_PORT : %s\nBROWSER_PORT : %d\nBUFFER_SIZE : %d\n\
		MAX_NO_OF_CONNECTIONS : %s\nROBOTS_INFO_DICT : %s\nDELIM : %s"
	 % (WELCOME_MSG, HOST, SERVER_PORT, BROWSER_PORT, BUFFER_SIZE,
	 	MAX_NO_OF_CONNECTIONS,ROBOTS_INFO_DICT,DELIM)"""

# Function to print the current time and the data
def printWithTime(data):
	print ("%s-->%s" %(time.asctime(), data))
	writeToFile(data)

# Function to write to a file.
def writeToFile(data):
	"""Write the status to a file.
	data : The data to be written.
	statusFileHandler : The global file handler for status file."""
	global statusFileHandler
	statusFileHandler.write ("%s-->%s" %(time.asctime(), data))

# Function to close the status file.
def closeFile():
	global statusFileHandler
	statusFileHandler.close()
	# NOTE - using print() instead of printWithTime(), as file handler
	# closed on previous statement.
	print ("Server status file : CLOSED.")

# 3. Function to get the robot name and its status
def getRobotNameAndStatus (conn, ip, port):
	try:
		""" Sending welcome message to the connected client at the new
		port- acknowledgement"""
		printWithTime ("Sending welcome message : %s" %(WELCOME_MSG))
		conn.send(WELCOME_MSG)
		print "Welcome message sent."
		data = conn.recv (BUFFER_SIZE)
		if data:
			printWithTime ("Data received : %s" % data)
			robotName, status = data.split(DELIM)
			status = status.strip()
			printWithTime ("%s :: Robot name : %s and current status: %s" %
				(str(ip),robotName,status))

			""" Add the robot data to the robots' info dictionary.
			Also, add the data to a file, for recovery process in
			case of a server crash. - Done in printWithTime()."""
			ROBOTS_INFO_DICT [robotName] = (ip,port,status)
			return robotName,status
		else:
			printWithTime ("No data received from robot")
		# DEBUG - add to file
	except socket.error, msg:
		printWithTime ("Error with IP : %s" % str(ip))
	except Exception as E:
		printWithTime ("Some exception while fetching robot name and status.")
		printWithTime (str(E))
	return None,None

# Function to handle communication with clients.
def clientThread(conn, ip, port, robotName):
	""" Continuously receive the data - robot's status. Breaking condition -
	if no data received in '5' seconds - declare robot as 'dead'."""
	printWithTime ("New thread for %s" % str(conn.getsockname()))
	while True:
		try:
			data = conn.recv (BUFFER_SIZE)
			if not data:
				break
			printWithTime ("Data received : %s" %data)
			robotName, status = data.split(DELIM)
			status.strip()
			ROBOTS_INFO_DICT[robotName] = (ip,port,status)
		except socket.error, (errNo,errMessage):
			printWithTime ("Error no : %d. Error Message : %s" % (errNo, errMessage))
			break
	printWithTime ("Closing connection with %s :: %s:%d." % (robotName,str(ip), port))
	conn.close()

# Send JSON data to browser
def sendToBrowser (conn, ip, port):
	try:
		printWithTime (("Sending Robots' information to browser::IP (%s:%d)") % 
			(str(ip), port))
		# If atleast 1 robot is present, send the robot info in JSON format.
		if (len (ROBOTS_INFO_DICT) > 0):
			ROBOTS_INFO_JSON = json.dumps (ROBOTS_INFO_DICT)
			conn.send (ROBOTS_INFO_JSON)
			printWithTime (('Robots info sent in JSON format to browser::IP (%s:%d).Closing connection.') % 
			(str(ip), port))
		# No robots available.
		else:
			conn.send("None")
			printWithTime (('No robots availble. None string sent to browser::IP (%s:%d).Closing connection.') % 
				(str(ip), port))
	except socket.error, msg:
		printWithTime (('Socket error with browser::IP (%s:%d).! Closing connection!') % 
			(str(ip), port))
	finally:
		conn.close()

# Function to close the server.
def closeServer(robotSocket, browserSocket):
	"""Close all the sockets.
	robotSocket : robot socket
	browserSocket : browser socket"""
	robotSocket.close()
	browserSocket.close()

# Start the server
def startServer():
	# Global variables.
	global SERVER_PORT, BROWSER_PORT
	try:

		# Create the sockets
		robotSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		browserSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# Bind the sockets
		robotSocket.bind ((HOST,SERVER_PORT))
		browserSocket.bind ((HOST, BROWSER_PORT))
		printWithTime ("Sockets binded successfully.")

		# Listen for incoming connections
		robotSocket.listen (MAX_NO_OF_CONNECTIONS)
		browserSocket.listen(MAX_NO_OF_CONNECTIONS)
		printWithTime ("Listening for incoming connections")
		
		return (robotSocket, browserSocket)
	except socket.error, msg:
		printWithTime ("Error while starting server.Error message : %s") % msg
		printWithTime ("Terminating.")
		closeFile()
		sys.exit(1)

# Main function
def main():

	# Initialising all the global variables and return file handler.
	init()
	
	""" Creating 3 lists for select() module.
		1. Input list
		2. Output list
		3. Error list"""
	# Start the server by creating sockets for robots and server.
	robotSocket,browserSocket = startServer()

	# Create an input sockets list
	inputs = [robotSocket,browserSocket]

	# Create an output socket list
	outputs = []

	printWithTime ("Server started.")
	printWithTime ("Server status file : OPENED.")
	"""
	1. Creates a socket for communication with the clients (robots).
	2. After accepting a call, communicates with the client on a separate
		port. on a separate thread."""

	printWithTime ("\t%s" % WELCOME_MSG)

	try:
		# 1. Wait for incoming connections
		while inputs:
			readable, writeable, exceptional = select.select (inputs, outputs, inputs)
			
			# Input channel
			for item in readable:
				# For server socket
				if item is robotSocket:
					""" accept() blocks the call - returns a new socket 
					object and address of the client."""
					conn, (ip,port) = robotSocket.accept()
					printWithTime (str (ip) + "::" + str(port) + "---ROBOT connection.")
					printWithTime ("Connected to : %s at port : %d" % (str(ip),port))
	
					# 2. Get the robot's name and its initial status
					robotName, status = getRobotNameAndStatus (conn,ip,port)
					# Robot connections
					if robotName is not None:
						# Start new thread
					    thread.start_new_thread (clientThread, (conn,str(ip),port,robotName,))
					
					# All other requests
					else:
						printWithTime ("Unknown connection at %s:%d. Terminating connection." %(str(ip),port))
						conn.close()

				# For browser socket
				elif item is browserSocket:
					conn, (ip,port) = browserSocket.accept()
					printWithTime (str (ip) + "::" + str(port) + "---BROWSER connection.")
					# Send the JSON data to the incoming browser connection.
					thread.start_new_thread (sendToBrowser, (conn,ip,port, ))
				else:
					printWithTime ("Unknown input connection. Terminating.")

			# Output channel
			for item in writeable:
				printWithTime ("%s available on output channel" %type(item))
				
			# Error channel
			for item in exceptional:
				printWithTime ("%s available on error channel" %type(item))
	# Socket error
	except socket.error, msg:
		printWithTime ("Socket error! Error-code : %s. Error-msg : %s" % (str(msg[0]),str(msg[1])))
	
	# In case of any exception, do not spawn a new thread
	except KeyboardInterrupt:
		printWithTime ("Keyboard interrupt!")

	except Exception,msg:
		printWithTime ("Exception while communicating with %s. Closing connection." %(str(ip)))
		conn.close()
		printWithTime ("Error Message : %s" %msg)
		printWithTime ("Error info : %s" % sys.exc_info()[2])

	# Close the socket
	finally:
		closeServer (robotSocket, browserSocket)
		printWithTime ("Server closed.")
		closeFile ()

if __name__ == "__main__":
	# Global variables
	WELCOME_MSG=""
	HOST=""
	SERVER_PORT=0
	BROWSER_PORT=0
	BUFFER_SIZE = 0
	MAX_NO_OF_CONNECTIONS=0
	ROBOTS_INFO_DICT = {}
	DELIM = ""
	SERVER_STATUS_FILE = "serverStatus.txt"
	statusFileHandler = None
	main()