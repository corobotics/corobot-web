import socket,sys,thread,traceback,time

# Function to initialize with default values
def init (WELCOME_MSG="", HOST="", PORT=0, BUFFER_SIZE=0, MAX_NO_OF_CONNECTIONS=0,
		ROBOTS_INFO_DICT={}, DELIM="",SERVER_STATUS_FILE=""):
	"""
	Includes variables for the default communication setup.
	If any of the parameters are not defined, use the mentioned default 
	ones.
	Returns : statusFileHandler: File handler for status logs."""

	if WELCOME_MSG == "" :
		WELCOME_MSG = "Welcome to corobotics server."
	if HOST == "":
		HOST = "129.21.30.80"
	if PORT == 0:
		PORT = 8081
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
	globals()["PORT"] = PORT
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	globals()["MAX_NO_OF_CONNECTIONS"] = MAX_NO_OF_CONNECTIONS
	globals()["ROBOTS_INFO_DICT"] = ROBOTS_INFO_DICT
	globals()["DELIM"] = DELIM
	globals()["SERVER_STATUS_FILE"] = SERVER_STATUS_FILE

	# Open server status file in append + reading mode
	statusFileHandler = open ("SERVER_STATUS_FILE","a+")

	# DEBUG 
	"""print ("Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\nPORT : %s\
	\nBUFFER_SIZE : %d\nMAX_NO_OF_CONNECTIONS : %s\nROBOTS_INFO_DICT : %s\
	\nDELIM : %s"
	 % (WELCOME_MSG,HOST,PORT,BUFFER_SIZE,MAX_NO_OF_CONNECTIONS,
		ROBOTS_INFO_DICT,DELIM)"""

	return statusFileHandler


# Function to send the status of all the robots to the browser.
def sendStatusToBrowser (conn):
	for robotName, (ip,port,status) in ROBOTS_INFO_DICT.iteritems():
		conn.send (robotName+DELIM+status)
	
# Function to print the current time and the data
def printWithTime(data):
	print ("%s-->%s" %(time.asctime(), data))

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
			# For a browser
			if robotName == "BROWSER":
				if len(ROBOTS_INFO_DICT) > 0:
					printWithTime ("Sending robots dict")
					sendStatusToBrowser (conn)
				else:
					printWithTime ("No robots available")
					conn.send ("None")
					return robotName, None
			# For other robots
			printWithTime ("%s :: Robot name : %s and current status: %s" %(str(ip),robotName,status))

			""" Add the robot data to the robots' info dictionary.
			Also, add the data to a file, for recovery process in
			case of a server crash."""
			ROBOTS_INFO_DICT [robotName] = (ip,port,status)
			return robotName,status
		else:
			printWithTime ("No data received from robot")

		# DEBUG - add to file
	except socket.error, msg:
		printWithTime ("Error with IP : %s" % str(ip))
	return None,None


# Function to handle communication with clients
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
			#print "Robot name : %s. Status is : %s" %(robotName,status)
		except socket.error, (errNo,errMessage):
			printWithTime ("Error no : %d. Error Message : %s" % (errNo, errMessage))
			break
	printWithTime ("Closing connection with %s :: %s:%d." % (robotName,str(ip), port))
	conn.close()

# Main function
def main():

	# Initialising all the global variables and return file handler.
	statusFileHandler = init()
	printWithTime ("Server started.")
	printWithTime ("Server status file : OPENED.")

	"""
	1. Creates a socket for communication with the clients (robots).
	2. After accepting a call, communicates with the client on a separate
		port. on a separate thread."""

	printWithTime ("\t%s" % WELCOME_MSG)

	# Creating a communication socket
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		# Bind the socket
		serverSocket.bind((HOST,PORT))
		printWithTime ("Server Socket binded successfully")
		# 0. Listen for incoming connections
		serverSocket.listen(MAX_NO_OF_CONNECTIONS)
		printWithTime ("Waiting for connection at port - %s" % str(PORT))

		# 1. Wait for incoming connections
		while True:
			""" accept() blocks the call - returns a new socket 
			object and address of the client."""

			try:
				conn,addr = serverSocket.accept()
				ip,port = addr
				printWithTime ("Connected to : %s at port : %d" % (str(ip),port))

				# 2. Get the robot's name and its initial status
				robotName, status = getRobotNameAndStatus (conn,ip,port)
				# Browser requests
				if robotName == "BROWSER":
					conn.close()
				# Robot connections
				elif robotName is not None:
					# Start new thread
				    thread.start_new_thread (clientThread, (conn,str(ip),port,robotName,))
				# All other requests
				else:
					printWithTime ("Unknown connection at %s:%d. Terminating connection.") %(str(ip),port)
					conn.close()
	
			# Socket error
			except socket.error, msg:
				printWithTime ("Sock error! Error-code : %s. Error-msg : %s" % (str(msg[0]),str(msg[1])))
				break
	
	# In case of any exception, do not spawn a new thread
	except Exception,msg:
		printWithTime ("Exception while communicating with %s. Closing connection." %(str(ip)))
		conn.close()
		printWithTime ("Error Message : %s" %msg)
		printWithTime ("Error info : %s" % sys.exc_info())

	except KeyboardInterrupt:
		printWithTime ("KeyboardInterrupt!")

	# Close the socket
	finally:
		serverSocket.close()
	statusFileHandler.close()
	printWithTime ("Server status file : CLOSED.")
	printWithTime ("Server closed.")

if __name__ == "__main__":
	# Global variables
	WELCOME_MSG=""
	HOST=""
	PORT=0
	BUFFER_SIZE = 0
	MAX_NO_OF_CONNECTIONS=0
	ROBOTS_INFO_DICT = {}
	DELIM = ""
	SERVER_STATUS_FILE = "serverStatus.txt"
	main()