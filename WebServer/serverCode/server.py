import socket,sys,thread,time,select,json,threading,subprocess,datetime
#from corobot import robot

# Function to initialize with default values
def init (WELCOME_MSG="", HOST="", ROBOT_PORT=0, CLIENT_PORT=0, BROWSER_PORT=0,
	BUFFER_SIZE=0,MAX_NO_OF_CONNECTIONS=0,ROBOTS_INFO_DICT={},DELIM="",
	SERVER_STATUS_FILE="", ROBOT_TIMEOUT=0):
	"""
	Includes variables for the default communication setup.
	If any of the parameters are not defined, use the mentioned default 
	ones."""
	# File handler for status file.
	global statusFileHandler, myLock

	myLock = threading.Lock()

	if WELCOME_MSG == "" :
		WELCOME_MSG = "Welcome to corobotics server."
	if HOST == "":
		HOST = "129.21.30.80"
	if ROBOT_PORT == 0:
		ROBOT_PORT = 51000
	if CLIENT_PORT == 0:
		CLIENT_PORT = 56000	
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
		SERVER_STATUS_FILE = "/home/robotics/Desktop/gitWebServer/corobot-web/WebServer/serverCode/serverStatusLog.txt"
		SERVER_STATUS_FILE += "-" + str(datetime.datetime.now().strftime ("%Y-%m-%d::%H:%M"))
	if ROBOT_TIMEOUT == 0:
		ROBOT_TIMEOUT = 10
	
	globals()["WELCOME_MSG"] = WELCOME_MSG
	globals()["HOST"] = HOST
	globals()["ROBOT_PORT"] = ROBOT_PORT
	globals()["CLIENT_PORT"] = CLIENT_PORT
	globals()["BROWSER_PORT"] = BROWSER_PORT
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	globals()["MAX_NO_OF_CONNECTIONS"] = MAX_NO_OF_CONNECTIONS
	globals()["ROBOTS_INFO_DICT"] = ROBOTS_INFO_DICT
	globals()["DELIM"] = DELIM
	globals()["SERVER_STATUS_FILE"] = SERVER_STATUS_FILE
	globals()["ROBOT_TIMEOUT"] = ROBOT_TIMEOUT


	# Open server status file in append + reading mode
	statusFileHandler = open (SERVER_STATUS_FILE,"a+")

	# DEBUG 
	"""printWithTime ("Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\n\
		ROBOT_PORT : %s\nCLIENT_PORT : %s\nBROWSER_PORT : %d\n \
		BUFFER_SIZE : %d\nMAX_NO_OF_CONNECTIONS : %s\nROBOTS_INFO_DICT : %s\n \
		DELIM : %s\nROBOT_TIMEOUT : %d" % (WELCOME_MSG, HOST, ROBOT_PORT,
		CLIENT_PORT, BROWSER_PORT,BUFFER_SIZE,MAX_NO_OF_CONNECTIONS,
		ROBOTS_INFO_DICT,DELIM, ROBOT_TIMEOUT)"""

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
	statusFileHandler.write ("\n%s-->%s." %(time.asctime(), data))

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
		printWithTime ("Sending welcome message : %s." % WELCOME_MSG)
		conn.sendall(WELCOME_MSG)
		printWithTime ("Welcome message sent.")
		data = conn.recv (BUFFER_SIZE)
		if data:
			printWithTime ("Data received : %s." % data)
			robotName, status = data.split(DELIM)
			status = status.strip()
			printWithTime ("%s :: Robot name : %s and current status: %s." % 
				(str(ip),robotName,status))

			""" Add the robot data to the robots' info dictionary.
			Also, add the data to a file, for recovery process in
			case of a server crash. - Done in printWithTime()."""
			ROBOTS_INFO_DICT [robotName] = (ip,port,status,-1,-1, time.time())
			return robotName,status
		else:
			printWithTime ("%s :: No data received from robot connection." % str(ip))
	
	except socket.error, (errNo,errMessage):
		printWithTime ("Error with IP : '%s'. Error code : %d. Error message : %s." % 
			(str(ip), errNo, errMessage))
	#except socket.error as msg:
		#printWithTime (msg + type(msg))
	except Exception as E:
		printWithTime ("Some exception while fetching robot name and status.")
		printWithTime (str(E))
	return None,None

# Function to handle communication with clients.
def clientThread(conn, ip, port, robotName):
	""" Continuously receive the data - robot's status. Breaking condition -
	if no data received in '5' seconds - declare robot as 'dead'."""
	printWithTime ("New thread for %s." % str(conn.getsockname()))
	while True:
		try:
			data = conn.recv (BUFFER_SIZE)
			if not data:
				break
			printWithTime ("'%s'::%s:Data received : %s." % 
				(str(ip),robotName, data))
			#robotName, status = data.split(DELIM)
			status,x,y = data.split (DELIM)
			status.strip()
			ROBOTS_INFO_DICT[robotName] = (ip,port,status, x,y, time.time())
		except ValueError:
			pass
		except socket.error, (errNo,errMessage):
			printWithTime ("Error no : %d. Error Message : %s." % 
				(errNo, errMessage))
		#except socket.error as msg:
			#printWithTime (msg + type(msg))
			break
	printWithTime ("Closing connection with %s :: (%s:%d)." % 
		(robotName,str(ip), port))
	conn.close()

# Function to check for DEAD robots.
def cleanupRobots():
	"""For all the robots in the ROBOTS_INFO_DICT, there is a check to determine
	if a robot is dead or not. This is done, by verifying the difference
	betweeen the timestamp of the last status of the robot and current timestamp
	to be within ROBOT_TIMEOUT."""
	try:
		global ROBOT_TIMEOUT
		now = int(time.time())
		printWithTime ("Trying to cleanup robots.")
		listOfRobotsToBeRemoved = list()
		if (len(ROBOTS_INFO_DICT) > 0):
			for robotName,attribList in ROBOTS_INFO_DICT.iteritems():
				robotTime = int(ROBOTS_INFO_DICT[robotName][5])
				diff = now - ROBOTS_INFO_DICT[robotName][5]
				printWithTime ("%s : Timestamp : %d Now : %d Diff : %d" % (robotName, robotTime, now,diff))
				if  (diff > ROBOT_TIMEOUT):
					listOfRobotsToBeRemoved.append (ROBOTS_INFO_DICT[robotName])
					printWithTime ("%s status expired. Will be removed." % robotName)
		for robotName in listOfRobotsToBeRemoved:
			ROBOTS_INFO_DICT.pop(robotName)
		time.sleep (5)
		cleanupRobots()
	except Exception as E:
		printWithTime (E)

# Send JSON data to browser
def sendToBrowser (conn, ip, port):
	try:
		printWithTime ("Sending Robots' information to browser::IP (%s:%d)." % 
			(str(ip), port))
		# If atleast 1 robot is present, send the robot info in JSON format.
		if (len (ROBOTS_INFO_DICT) > 0):
			ROBOTS_INFO_JSON = json.dumps (ROBOTS_INFO_DICT)
			conn.send (ROBOTS_INFO_JSON)
			printWithTime ("Robots info sent in JSON format to browser::IP (%s:%d). Closing connection!" % 
				(str(ip), port))
		# No robots available.
		else:
			#conn.send("None")
			ROBOTS_INFO_JSON = json.dumps (ROBOTS_INFO_DICT)
			conn.sendall (ROBOTS_INFO_JSON)			
			printWithTime ("No robots availble. None string sent to browser::IP (%s:%d). Closing connection!" % 
				(str(ip), port))
	except socket.error, (errNo,errMessage):
		printWithTime ("Socket error with browser::IP (%s:%d)! Error no : %d. Error Message : %s. Closing connection!" %
			(str(ip), port, errNo, errMessage))
	#except socket.error as msg:
		#printWithTime (msg + type(msg))
	finally:
		conn.close()

# Function returns the count of IDLE robots
def getIdleRobotCount ():
	totalRobots = len(ROBOTS_INFO_DICT)
	count = 0
	printWithTime ("Total robots : %d " % totalRobots)
	if (totalRobots > 0):
		for attribList in ROBOTS_INFO_DICT.itervalues():
			status = attribList[2]
			if (status.upper() == "IDLE"):
				count += 1
	else:
		printWithTime ("No robots in the system.")
	return count

# Function to get an IDLE robot from ROBOTS_INFO_DICT
def getIdleRobot ():
	# Check if there exists atleast 1 robot.
	if (len (ROBOTS_INFO_DICT) > 0):
		for robotName, attribList in ROBOTS_INFO_DICT.iteritems():
			if (attribList[2].upper() == "IDLE"):
				return robotName, attribList
	else:
		return None, None

# Function to cater to a client request. Assign an IDLE robot to a client.
def assignRobot (conn, ip, port):
	"""
	conn : socket object of the client.
	ip : ip address of the client.
	port : port address of the client.

	Returns : robotName - Assigned IDLE robot. If no IDLE robots available,
		return None."""

	robotName = None
	try:
		destination = conn.recv (1024)
		# If no destination received.
		if not destination:
			printWithTime ("%s::No destination received. Closing connection!" % str(ip))
		# Some destination received.
		else:
			printWithTime ("%s::Destination to be assigned : %s. No of IDLE robots : %d." % (str(ip),destination, getIdleRobotCount()))
			robotName, attribList = getIdleRobot()
			if robotName is not None:
				conn.sendall ("Idle robot found. Robot name : %s." % robotName)
				printWithTime ("%s::Idle robot found. Robot name : %s" % (str(ip), robotName))
				# Send the IP of the robot
			else:
				conn.sendall ("Sorry. Unable to assign a robot. Closing connection!")
				printWithTime ("%s::Sorry. Unable to assign a robot. Closing connection!" % str(ip))
	except socket.error, (errNo,errMessage):
		printWithTime ("Socket error with browser::IP (%s:%d)! Error no : %d. Error Message : %s. Closing connection!" %
			(str(ip), port, errNo, errMessage))
	#except socket.error as msg:
		#printWithTime (msg + type(msg))
	finally:
		printWithTime ("Closing connection with CLIENT :: (%s:%d)." % (str(ip), port))
		# Deploy the code for the assigned robot
		if robotName is not None:
			#conn.sendall ("Deploying code on IP (%s)." % attribList[0])
			printWithTime ("%s::Deploying code on IP (%s) Robot name : %s." % (str(ip), attribList[0], robotName))
			conn.sendall ("Please check the status on our webpage : www.vhost1.cs.rit.edu/status.php")
			conn.close()
			deployCode (robotName, attribList[0], destination)

# Function to deploy code on a robot
def deployCode(robotName, ip, destination):
	printWithTime ("Deploying code on %s, Destination : %s." % (robotName, destination))
	subprocess.call (["python3", "new.py", ip, destination])

# Function to close the server.
def closeServer(robotSocket, clientSocket, browserSocket):
	"""Close all the sockets.
	robotSocket : robot socket
	clientSocket : client socket
	browserSocket : browser socket"""
	robotSocket.close()
	clientSocket.close()
	browserSocket.close()

# Start the server
def startServer():
	# Global variables.
	global ROBOT_PORT, CLIENT_PORT, BROWSER_PORT
	try:

		# Create the sockets
		robotSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		browserSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# Bind the sockets
		robotSocket.bind ((HOST,ROBOT_PORT))
		clientSocket.bind ((HOST,CLIENT_PORT))
		browserSocket.bind ((HOST, BROWSER_PORT))
		printWithTime ("Sockets binded successfully.")
		printWithTime ("Robot socket at port : %d" % ROBOT_PORT)
		printWithTime ("Client socket at port : %d" % CLIENT_PORT)
		printWithTime ("Browser socket at port : %d" % BROWSER_PORT)

		# Listen for incoming connections
		robotSocket.listen (MAX_NO_OF_CONNECTIONS)
		clientSocket.listen (MAX_NO_OF_CONNECTIONS)
		browserSocket.listen(MAX_NO_OF_CONNECTIONS)
		printWithTime ("Listening for incoming connections.")
		
		return (robotSocket,clientSocket, browserSocket)
	except socket.error, (errNo, errMessage):
		printWithTime ("Error while starting server. Error code : %d. Error message : %s. Terminating!!!" %
			(errNo, errMessage))
	#except socket.error as msg:
		#printWithTime (msg + type(msg))
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
	robotSocket,clientSocket,browserSocket = startServer()

	# Create an input sockets list
	inputs = [robotSocket,clientSocket,browserSocket]

	# Create an output socket list
	outputs = []

	printWithTime ("Server started.")
	printWithTime ("Server status file : OPENED.")
	"""
	1. Creates a socket for communication with the clients (robots).
	2. After accepting a call, communicates with the client on a separate
		port. on a separate thread."""

	printWithTime ("\t%s" % WELCOME_MSG)

	# Start the timer to clean-up dead robots
	#thread.start_new_thread (cleanupRobots, ())

	try:
		# 1. Wait for incoming connections
		while inputs:
			readable, writeable, exceptional = select.select (inputs, outputs, inputs)
			
			# Input channel
			for item in readable:
				# For robot socket
				if item is robotSocket:
					""" accept() blocks the call - returns a new socket 
					object and address of the client."""
					conn, (ip,port) = robotSocket.accept()
					#printWithTime ("%s::%d ---ROBOT connection." % (str(ip), port))
	
					# 2. Get the robot's name and its initial status
					robotName, status = getRobotNameAndStatus (conn,ip,port)
					# Robot connections
					if robotName is not None:
						# Start new thread
					    thread.start_new_thread (clientThread, (conn,str(ip),port,robotName,))
					
					# All other requests
					else:
						printWithTime ("Unknown connection at %s:%d. Terminating connection." %
							(str(ip),port))
						conn.close()

				# For client socket
				elif item is clientSocket:
					conn, (ip,port) = clientSocket.accept()
					printWithTime ("%s::%d ---CLIENT connection." % (str(ip), port))
					
					# Accept the commands from the client.
					thread.start_new_thread (assignRobot, (conn,ip,port, ))

				# For browser socket
				elif item is browserSocket:
					conn, (ip,port) = browserSocket.accept()
					#printWithTime ("%s::%d ---BROWSER connection." % (str(ip), port))
					#conn.close()
					# Send the JSON data to the incoming browser connection.
					thread.start_new_thread (sendToBrowser, (conn,ip,port, ))
				else:
					printWithTime ("Unknown input connection. Closing connection!")
					conn.close()

			# Output channel
			for item in writeable:
				printWithTime ("%s available on output channel." % type(item))
				
			# Error channel
			for item in exceptional:
				printWithTime ("%s available on error channel." % type(item))

	# Socket error
	except socket.error, (errNo, errMessage):
		printWithTime ("Socket error! Error code : %d. Error message : %s." % (errNo, errMessage))
	#except socket.error as msg:
		#printWithTime (msg + type(msg))

	
	# In case of any exception, do not spawn a new thread
	except KeyboardInterrupt:
		printWithTime ("Keyboard interrupt!")

	#except Exception,(errNo, errMessage):
		#printWithTime ("Exception while communicating with %s. Error code : %d. Error message : %s. Closing connection!" % 
			#(str(ip), errNo, errMessage))
	except Exception as msg:
		printWithTime (msg + type(msg))
		conn.close()

	# Close the socket
	finally:
		closeServer (robotSocket, clientSocket,browserSocket)
		printWithTime ("Server closed.")
		closeFile ()

if __name__ == "__main__":
	# Global variables
	WELCOME_MSG=""
	HOST=""
	ROBOT_PORT=0
	BROWSER_PORT=0
	BUFFER_SIZE = 0
	MAX_NO_OF_CONNECTIONS=0
	ROBOTS_INFO_DICT = {}
	DELIM = ""
	SERVER_STATUS_FILE = "serverStatus.txt"
	statusFileHandler = None
	ROBOT_TIMEOUT = 0
	main()