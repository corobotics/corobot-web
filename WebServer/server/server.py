import socket,sys,thread,traceback

# Function to initialize with default values
def init (WELCOME_MSG="", HOST="", PORT=0, BUFFER_SIZE=0, 
		MAX_NO_OF_CONNECTIONS=0,ROBOTS_INFO_DICT=None):
	"""
	Includes variables for the default communication setup.
	If any of the parameters are not defined, use the mentioned default 
	ones"""

	if WELCOME_MSG == "" :
		WELCOME_MSG = "Welcome to corobotics server."
	if HOST == "":
		HOST = "129.21.30.80"
	if PORT == 0:
		PORT = 8080
	if BUFFER_SIZE == 0:
		BUFFER_SIZE = 4096
	if MAX_NO_OF_CONNECTIONS == 0:
		MAX_NO_OF_CONNECTIONS = 10
	if ROBOTS_INFO_DICT == None:
		ROBOTS_INFO_DICT = {}
	
	globals()["WELCOME_MSG"] = WELCOME_MSG
	globals()["HOST"] = HOST
	globals()["PORT"] = PORT
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	globals()["MAX_NO_OF_CONNECTIONS"] = MAX_NO_OF_CONNECTIONS
	globals()["ROBOTS_INFO_DICT"] = ROBOTS_INFO_DICT

	# DEBUG 
	"""print ("Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\nPORT : %s\
	\nBUFFER_SIZE : %d\nMAX_NO_OF_CONNECTIONS : %s\nROBOTS_INFO_DICT : %s")
	 % (WELCOME_MSG,HOST,PORT,BUFFER_SIZE,MAX_NO_OF_CONNECTIONS,
		ROBOTS_INFO_DICT)"""

# 3. Function to get the robot name and its status
def getRobotNameAndStatus (conn, ip, port):
        try:
                """ Sending welcome message to the connected client at the new
		 port- acknowledgement"""

                print "Sending welcome message : %s" %(WELCOME_MSG)
                conn.send(WELCOME_MSG)
                print "Welcome message sent."
                data = conn.recv (BUFFER_SIZE)
		if data:
			print "Data received : %s" %data

		        robot_name, status = data.split("-")
			status = status.strip()
		        print "%s :: Robot name : %s and current status: %s" \
				%(str(ip),robot_name,status)

		        """ Add the robot data to the robots' info dictionary.
			Also, add the data to a file, for recovery process in
			case of a server crash."""
		        ROBOTS_INFO_DICT [robot_name] = (ip,port,status)
		        return robot_name,status
		else:
			print "No data received from robot"
		
		# DEBUG - add to file
                
        except socket.error, msg:
                print "Error with IP : %s" % str(ip)
	return None,None

# Function to print the current robot status.
def printRobotStatusThread ():
	print "Current Robots Status- "
	for robot_name,text in ROBOTS_INFO_DICT.iteritems():
		print "Robot Name : %s\tCurrent Status : %s" % (robot_name,text)


# Function to handle communication with clients
def clientThread(conn, ip, port, robot_name):
	
	""" Continuously receive the data - robot's status. Breaking condition -
	if no data received in '5' seconds - declare robot as 'dead'."""
	while True:
		data = conn.recv (BUFFER_SIZE)
		if not data:
			break
		#print "Data received : %s" %data
		robot_name, status = data.split("-")
		status.strip()
		ROBOTS_INFO_DICT[robot_name] = ip,port,status
		#print "Robot name : %s. Status is : %s" %(robot_name,status)
	print "Closing connection with %s :: %s:%d." % (robot_name,str(ip), port)
	conn.close()

# Main function
def main():

	"""
	1. Creates a socket for communication with the clients (robots).
	2. After accepting a call, communicates with the client on a separate
		port. on a separate thread."""

	init()
	print "\t%s" % WELCOME_MSG

	# Creating a communication socket
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # 0. Bind the socket
        try:
                s.bind((HOST,PORT))
                print "Socket binded successfully"

                # 0. Listen for incoming connections
                print "Waiting for connection at port - %s" % str(PORT)
                s.listen(MAX_NO_OF_CONNECTIONS)

                # 1. Wait for incoming connections
                while True:
                        """ accept() blocks the call - returns a new socket 
			object and address of the client."""

                        try:
                                conn,addr = s.accept()
                                ip,new_port = addr
                                print "Connected to : %s at port : " \
					% str(ip),str(new_port)

				# 2. Get the robot's name and its initial status
				robot_name, status = getRobotNameAndStatus \
							(conn,ip,new_port)

				# Start new thread
		                thread.start_new_thread (clientThread,
						 (conn,str(ip),new_port,robot_name,))

			# In case of any exception, do not spawn a new thread
			except Exception, msg:
				print "Exception while communicating with"\
					" %s. Closing connection." %(str(ip))
				conn.close()
				print "Error Message : %s" %msg
				print "More info : %s" % sys.exc_info()[2]
                      
        except socket.error, msg:
                print "Sock error! Error-code : %s.Error-msg :%s"\
			% (str(msg[0]),str(msg[1]))
                sys.exit(1)

        finally:
                s.close()

if __name__ == "__main__":

	WELCOME_MSG=""
	HOST=""
	PORT=0
	BUFFER_SIZE = 0
	MAX_NO_OF_CONNECTIONS=0
	ROBOTS_INFO_DICT = {}

	main()
