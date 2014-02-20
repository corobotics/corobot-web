import socket,sys,thread,time,select,json,threading,subprocess,datetime

# 0. Function to initialize with default values
def init (WELCOME_MSG="", HOST="", ROBOT_PORT=0, CLIENT_PORT=0, BROWSER_PORT=0,
	CLIENT_IP_PORT=0, BUFFER_SIZE=0, MAX_NO_OF_CONNECTIONS=0,ROBOTS_INFO_DICT={},
	DELIM="",SERVER_STATUS_FILE="", ROBOT_TIMEOUT=0, FREQUENCY=0):
	"""
	Includes variables for the default communication setup.
	Initializes the parameters. 

	WELCOME_MSG 			: Welcome message that is sent to the robots on the 
								first attempt of connection.
	HOST 					: Hostname
	PORT 					: Host port no.
	ROBOT_PORT 				: Port no. for robot connections.
	CLIENT_PORT 			: Port no. for client connections.
	BROWSER_PORT 			: Port no. for browser connections.
	CLIENT_IP_PORT 			: Port no. for client-IP-only connections.
	BUFFER_SIZE 			: Buffer size for socket communication.
	MAX_NO_OF_CONNECTIONS 	: Max no. of connections a socket can listen to.
	ROBOTS_INFO_DICT 		: Dictionary containing all the information about 
								robots.
								Format : <robot-name> : <robot attributes>
										 <robot-name> : Name of the robot.
										 <robot attributes> : List of a robot's
										 current attributes. 
										[ip, port, status, x-position, 
										y-position, destination, timestamp]
	DELIM 					: Delimiter of data sent from robots.
	SERVER_STATUS_FILE 		: Name of the server status log file.
	ROBOT_TIMEOUT 			: Timeout in seconds for robot status.
	FREQUENCY 				: Frequency of dead robot cleanup method in seconds.
	"""
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
	if CLIENT_IP_PORT == 0:
		CLIENT_IP_PORT = 65000	
	if BUFFER_SIZE == 0:
		BUFFER_SIZE = 4096
	if MAX_NO_OF_CONNECTIONS == 0:
		MAX_NO_OF_CONNECTIONS = 10
	if ROBOTS_INFO_DICT == {}:
		ROBOTS_INFO_DICT = {}
	if DELIM == "":
		DELIM = ":"
	if SERVER_STATUS_FILE == "":
		directory = "/home/robotics/Desktop/gitWebServer/corobot-web/WebServer/serverCode/"
		SERVER_STATUS_FILE = directory + "serverStatusLog" + "-" + str(datetime.datetime.now().strftime ("%Y-%m-%d::%H:%M")) + ".txt"
	if ROBOT_TIMEOUT == 0:
		ROBOT_TIMEOUT = 10
	if FREQUENCY == 0:
		FREQUENCY = 15

	globals()["WELCOME_MSG"] = WELCOME_MSG
	globals()["HOST"] = HOST
	globals()["ROBOT_PORT"] = ROBOT_PORT
	globals()["CLIENT_PORT"] = CLIENT_PORT
	globals()["BROWSER_PORT"] = BROWSER_PORT
	globals()["CLIENT_IP_PORT"] = CLIENT_IP_PORT
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	globals()["MAX_NO_OF_CONNECTIONS"] = MAX_NO_OF_CONNECTIONS
	globals()["ROBOTS_INFO_DICT"] = ROBOTS_INFO_DICT
	globals()["DELIM"] = DELIM
	globals()["SERVER_STATUS_FILE"] = SERVER_STATUS_FILE
	globals()["ROBOT_TIMEOUT"] = ROBOT_TIMEOUT
	globals()["FREQUENCY"] = FREQUENCY


	# Open server status file in append + reading mode
	statusFileHandler = open (SERVER_STATUS_FILE,"a+")

	# DEBUG 
	"""printWithTime ("Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\n\
		ROBOT_PORT : %s\nCLIENT_PORT : %s\nBROWSER_PORT : %d\n \
		BUFFER_SIZE : %d\nMAX_NO_OF_CONNECTIONS : %s\nROBOTS_INFO_DICT : %s\n \
		DELIM : %s\nROBOT_TIMEOUT : %d" % (WELCOME_MSG, HOST, ROBOT_PORT,
		CLIENT_PORT, BROWSER_PORT,BUFFER_SIZE,MAX_NO_OF_CONNECTIONS,
		ROBOTS_INFO_DICT,DELIM, ROBOT_TIMEOUT)"""

# 0. Function to print the current time and the data
def printWithTime(data):
	"""Function prints data to console with current time. Also forwards the same
	to the file.
	data : The data to printed and written to file."""
	print ("%s-->%s" %(time.asctime(), data))
	writeToFile(data)

# 0. Function to write to a file.
def writeToFile(data):
	"""Write the status to a file.
	data : The data to be written.
	statusFileHandler : The global file handler for status file."""
	global statusFileHandler
	statusFileHandler.write ("\n%s-->%s." %(time.asctime(), data))

# 13. Function to close the server.
def closeServer(robotSocket, clientSocket, browserSocket):
	"""Close all the sockets.
	robotSocket : robot socket
	clientSocket : client socket
	browserSocket : browser socket"""
	robotSocket.close()
	clientSocket.close()
	browserSocket.close()

# 12. Function to return IP of an IDLE robot.
def getIdleRobotIP(conn, ip, port):
	robotName, attribList = getIdleRobot()
	try:
		if robotName is not None:
			idleRobotIP = attribList[0]
			conn.sendall(idleRobotIP)
		else:
			conn.sendall ("None")
	except socket.error, (errNo,errMessage):
		printWithTime ("Socket error with client-IP-only socket::IP (%s:%d)! Error no : %d. Error Message : %s. Closing connection!" %
			(str(ip), port, errNo, errMessage))
	finally:
		printWithTime ("Closing client-IP-only connection :: (%s:%d)." % (str(ip), port))
		conn.close()

# 11. Function to send JSON data to browser.
def sendToBrowser (conn, ip, port):
	"""Function to send the robots info dictionary in JSON format to a browser.
	conn : The socket connection object to the browser.
	ip : IP address of the browser 'conn' is connected to.
	port : Port address of the browser 'conn' is connected to."""
	global ROBOTS_INFO_DICT

	try:
		printWithTime ("Sending Robots' information to browser::IP (%s:%d)." % 
			(str(ip), port))
		# If atleast 1 robot is present, send output in JSON format. Else, 'none' is sent.
		ROBOTS_INFO_JSON = json.dumps (ROBOTS_INFO_DICT)
		conn.sendall (ROBOTS_INFO_JSON)
		if (len (ROBOTS_INFO_DICT) > 0):
			printWithTime ("Robots info sent in JSON format to browser::IP (%s:%d). Closing connection!" % 
				(str(ip), port))
		# No robots available.
		else:
			printWithTime ("No robots availble. None string sent to browser::IP (%s:%d). Closing connection!" % 
				(str(ip), port))
	except socket.error, (errNo,errMessage):
		printWithTime ("Socket error with browser::IP (%s:%d)! Error no : %d. Error Message : %s. Closing connection!" %
			(str(ip), port, errNo, errMessage))
	finally:
		conn.close()

# 10. Function to deploy code on a robot
def deployCode(robotName, ip, destination):
	"""Function deploys the "destination" to the "robotName".
	robotName : Name of the robot to which the code is deployed.
	ip : IP address of the robot with name - "robotName".
	destination : A string for the "nav_to.py" program."""

	printWithTime ("Deploying code on %s, Destination : %s." % (robotName, destination))
	subprocess.call (["python3", "new.py", ip, destination])
	#subprocess.call (["python3", "nav_to.py", ip, destination])

# 9. Function to get an IDLE robot from ROBOTS_INFO_DICT
def getIdleRobot():
	"""Function to return a currently available 'idle' robot.
	Returns :  robotName - Name of the 'idle' robot and attribList - its 
				attributes.
				If no 'idle' robots are available, return 'None, None'."""
	global ROBOTS_INFO_DICT

	# Check if there exists atleast 1 robot.
	if (getIdleRobotCount() > 0):
		for robotName, attribList in ROBOTS_INFO_DICT.iteritems():
			#if (attribList[2].upper() == "IDLE"):
			return robotName, attribList
	else:
		return None, None

# 8. Function returns the count of IDLE robots
def getIdleRobotCount ():
	"""Function returns count of the currently 'idle' robots in the system."""

	global ROBOTS_INFO_DICT

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

# 7. Function to cater to a client request. Assign an IDLE robot to a client.
def assignRobot (conn, ip, port):
	"""Function to assign an 'idle' robot to a client. It also stores the 
		destination in the ROBOTS_INFO_DICT dictionary.
	conn : socket object of the client.
	ip : ip address of the client.
	port : port address of the client.

	Returns : robotName - Assigned IDLE robot. If no IDLE robots available,
		return None."""
	global ROBOTS_INFO_DICT
	robotName = None
	try:
		destination = conn.recv (BUFFER_SIZE)
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
				# Store the destination in the robots info dictionary.
				ROBOTS_INFO_DICT[robotName][5] = destination

			else:
				conn.sendall ("Sorry. Unable to assign a robot. Closing connection!")
				printWithTime ("%s::Sorry. Unable to assign a robot. Closing connection!" % str(ip))
	except socket.error, (errNo,errMessage):
		printWithTime ("Socket error with browser::IP (%s:%d)! Error no : %d. Error Message : %s. Closing connection!" %
			(str(ip), port, errNo, errMessage))
	#except socket.error as msg:
		#printWithTime (msg + type(msg))
	finally:
		# Deploy the code for the assigned robot
		if robotName is not None:
			conn.sendall("%s::Deploying code on IP (%s) Robot name : %s." % (str(ip), attribList[0], robotName))
			printWithTime ("%s::Deploying code on IP (%s) Robot name : %s." % (str(ip), attribList[0], robotName))
			conn.sendall ("Please check the status on our webpage : www.vhost1.cs.rit.edu/status.php")
			deployCode (robotName, attribList[0], destination)
		printWithTime ("Closing connection with CLIENT :: (%s:%d)." % (str(ip), port))
		conn.close()

# 6. Function to handle communication with clients.
def clientThread(conn, ip, port, robotName):
	"""Function to continuously receive the data - robot's status.
	conn - Socket connection to client.
	ip :  IP address of the client.
	port : Port address of the client.
	robotName - Name of the connected robot."""
	
	global ROBOTS_INFO_DICT

	printWithTime ("New thread for %s." % str(conn.getsockname()))
	while True:
		try:
			data = conn.recv (BUFFER_SIZE)
			if not data:
				break
			printWithTime ("'%s'::%s:Data received : %s." % 
				(str(ip),robotName, data))
			status,x,y = data.split (DELIM)
			status.strip()
			#ROBOTS_INFO_DICT[robotName] = (ip,port,status, x,y, "-", time.time())
			ROBOTS_INFO_DICT[robotName][2] = status
			ROBOTS_INFO_DICT[robotName][3] = x
			ROBOTS_INFO_DICT[robotName][4] = y
			ROBOTS_INFO_DICT[robotName][-1] = time.time()
		except ValueError:
			pass
		except socket.error, (errNo,errMessage):
			printWithTime ("Error no : %d. Error Message : %s." % 
				(errNo, errMessage))
			break
	printWithTime ("Closing connection with %s :: (%s:%d)." % 
		(robotName,str(ip), port))
	conn.close()

# 5. Function to get the robot name and its status
def getRobotNameAndStatus (conn, ip, port):
	"""Function to get the robot name and its status.
	conn : Socket connection object of the robot.
	ip : IP address of the robot.
	port : Port address of the robot."""

	global ROBOTS_INFO_DICT
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
			ROBOTS_INFO_DICT [robotName] = [ip,port,status,-1,-1,"-", time.time()]
			return robotName,status
		else:
			printWithTime ("%s :: No data received from robot connection." % str(ip))
	
	except socket.error, (errNo,errMessage):
		printWithTime ("Error with IP : '%s'. Error code : %d. Error message : %s." % 
			(str(ip), errNo, errMessage))
	except Exception as E:
		printWithTime ("Some exception while fetching robot name and status.")
		printWithTime (str(E))
	return None,None

# 4. Function to check for DEAD robots.
def cleanupRobots():
	"""For all the robots in the ROBOTS_INFO_DICT, there is a check to determine
	if a robot is dead or not. This is done, by verifying the difference
	betweeen the timestamp of the last status of the robot and the current
	timestamp. 
	Robot time : int(ROBOTS_INFO_DICT[robotName][-1])
	Current time : int(time.time())
	The max.difference should be within ROBOT_TIMEOUT.
	"""
	# Frequency of clean up operation.
	#frequency = 15
	try:
		global ROBOT_TIMEOUT, ROBOTS_INFO_DICT
		printWithTime ("Trying to cleanup robots.")
		listOfRobotsToBeRemoved = list()
		if (len(ROBOTS_INFO_DICT) > 0):
			for robotName,attribList in ROBOTS_INFO_DICT.iteritems():
				robotTime = int(ROBOTS_INFO_DICT[robotName][-1])
				now = int(time.time())
				diff = now - robotTime
				printWithTime ("%s :: Timestamp : %d. Now : %d. Diff : %d." % (robotName, robotTime, now, diff))
				if  (diff > ROBOT_TIMEOUT):
					listOfRobotsToBeRemoved.append (robotName)
					printWithTime ("%s status expired. Will be removed." % robotName)
			for robotName in listOfRobotsToBeRemoved:
				ROBOTS_INFO_DICT.pop(robotName)
		else:
			printWithTime ("No robots to clean.")
	except Exception as E:
		printWithTime (E)
	"""
	finally:
		time.sleep (frequency)
		cleanupRobots()"""

# 3. Function to repeatedly call another function.
def repeat (frequency, functionName):
	try:
		threading.Timer (frequency,repeat, [frequency, functionName]).start()
		functionName()
	except Exception as E:
		printWithTime (E)


# 2. Function to close the status file.
def closeFile():
	""" Function to close the server status file."""

	global statusFileHandler
	statusFileHandler.close()
	# NOTE - using print() instead of printWithTime(), as file handler
	# closed on previous statement.
	print ("Server status file : CLOSED.")

# 1. Start the server
def startServer():
	""" Function to start the server. Following operations are performed for
	robots, clients and browser connections - 
	1. Creating sockets
	2. Binding sockets
	Returns : A tuple containing sockets for all the connections."""
	
	# Global variables.
	global ROBOT_PORT, CLIENT_PORT, BROWSER_PORT
	try:

		# Create the sockets
		robotSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		browserSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		# This will be the permanent socket for Robot() for clients.
		clientIPOnlySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		# Bind the sockets
		robotSocket.bind ((HOST,ROBOT_PORT))
		clientSocket.bind ((HOST,CLIENT_PORT))
		browserSocket.bind ((HOST, BROWSER_PORT))
		clientIPOnlySocket.bind ((HOST, CLIENT_IP_PORT))

		printWithTime ("Sockets binded successfully.")
		printWithTime ("Robot socket at port : %d" % ROBOT_PORT)
		printWithTime ("Client socket at port : %d" % CLIENT_PORT)
		printWithTime ("Browser socket at port : %d" % BROWSER_PORT)
		printWithTime ("Client-IP-only socket at port : %d" % CLIENT_IP_PORT)

		# Listen for incoming connections
		robotSocket.listen (MAX_NO_OF_CONNECTIONS)
		clientSocket.listen (MAX_NO_OF_CONNECTIONS)
		browserSocket.listen (MAX_NO_OF_CONNECTIONS)
		clientIPOnlySocket.listen (MAX_NO_OF_CONNECTIONS)
		printWithTime ("Listening for incoming connections.")
		
		return (robotSocket,clientSocket, browserSocket, clientIPOnlySocket)
	except socket.error, (errNo, errMessage):
		printWithTime ("Error while starting server. Error code : %d. Error message : %s. Terminating!!!" %
			(errNo, errMessage))
		closeFile()
		sys.exit(1)

# 0. Main function
def main():

	# Initialising all the global variables and return file handler.
	init()
	
	""" Creating 3 lists for select() module.
		1. Input list
		2. Output list
		3. Error list"""
	# Start the server by creating sockets for robots and server.
	robotSocket,clientSocket,browserSocket,clientIPOnlySocket = startServer()

	# Create an input sockets list
	inputs = [robotSocket,clientSocket,browserSocket,clientIPOnlySocket]

	# Create an output socket list
	outputs = []

	printWithTime ("Server started.")
	printWithTime ("Server status file : OPENED.")
	printWithTime ("Status log file name : %s" % SERVER_STATUS_FILE)
	printWithTime ("\t%s" % WELCOME_MSG)

	# Function to repeat cleanupRobots() forever with interval of 'frequency' seconds
	repeat(FREQUENCY,cleanupRobots)

	try:
		# Wait for incoming connections.
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
					thread.start_new_thread (assignRobot, (conn,ip,port,))

				# For browser socket
				elif item is browserSocket:
					conn, (ip,port) = browserSocket.accept()

					# Send the JSON data to the incoming browser connection.
					thread.start_new_thread (sendToBrowser, (conn,ip,port,))

				# For client-IP-only sockets.
				elif item is clientIPOnlySocket:
					conn,(ip,port) = clientIPOnlySocket.accept()
					printWithTime ("%s::%d ---client-IP-only connection." % (str(ip), port))
					
					# Accept the commands from the client-IP-only sockets.
					thread.start_new_thread (getIdleRobotIP, (conn,ip,port,))

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
	CLIENT_PORT = 0
	BROWSER_PORT=0
	CLIENT_IP_PORT = 0
	BUFFER_SIZE = 0
	MAX_NO_OF_CONNECTIONS=0
	ROBOTS_INFO_DICT = {}
	DELIM = ""
	SERVER_STATUS_FILE = "serverStatus.txt"
	ROBOT_TIMEOUT = 0
	FREQUENCY = 0
	statusFileHandler = None
	main()