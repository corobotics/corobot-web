import socket, sys

# Function to initialize with default values
def init (WELCOME_MSG="", HOST="", PORT=0, ROBOT_NAME="", STATUS="", BUFFER_SIZE=0):
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
	if ROBOT_NAME == "":
		ROBOT_NAME = "Robot 1"
	if STATUS == "":
		STATUS = "IDLE"
	if BUFFER_SIZE == 0:
		BUFFER_SIZE = 4096
	
	globals()["WELCOME_MSG"] = WELCOME_MSG
	globals()["HOST"] = HOST
	globals()["PORT"] = PORT
	globals()["ROBOT_NAME"] = ROBOT_NAME
	globals()["STATUS"] = STATUS
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	
	# DEBUG 
	"""print "Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\nPORT : %s\
	\nROBOT_NAME : %s\nSTATUS : %s\nBUFFER_SIZE : %s" % (WELCOME_MSG, HOST,
	PORT,ROBOT_NAME,STATUS,BUFFER_SIZE)"""

""" Function to communicate with the server. Continuously send the status to the 
server."""

def communicate (conn):
	statusList = ("BUSY", "IDLE")
	i = 0
	count = 0
	try:
		while count < 10:
			conn.sendall(ROBOT_NAME + "-" + statusList[i])
			i += 1
			if i > 1:
				i=0
			count += 1
	except socket.error, msg:
		print "Error while receiving data. Error message : %s" %(msg)

# Main function
def main ():
	
	# Set the default values
	init()
	
	print "\t---%s TERMINAL---" %(ROBOT_NAME)
	
	# Create a communicating socket
	try:
	    #create an AF_INET, STREAM socket (TCP)
	    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
	    print "Failed to create socket. Error code: " + str(msg[0]) \
		+ " , Error message : " + msg[1]
	    sys.exit()
	 
	print "Socket Created"
	
	# 2. Communicate with remote server - HANDSHAKE
	try:
		conn.connect((HOST , PORT)) 
		print "Socket connected to " + HOST + " at port : " + str(PORT)

		# Blocking call
		data = conn.recv (BUFFER_SIZE)
		print "Data received : %s" %(data)
		print "Required : %s" %(WELCOME_MSG)
		if data == WELCOME_MSG:
			# Connection was successful
			print "Successful handshake"
			message = ROBOT_NAME + "-" + STATUS
	    
		    	# 3. Send the robot name and initial status
		    	print "Sending message : " + message
		    	conn.sendall(message)
			print "Message sent : %s" %message

			# 4. Now continuously communicate with server.
			communicate (conn)
			
		else:
			print "Incorrect data received from server.\nData : %s \
			" %(data)
				    	
	except socket.error,message:
		print "Error while receiving ack from server. Aborting."
		conn.close()
	except Exception, msg:
		print "Exception. More messages : " + sys.exc_info()[2]
		conn.close()
	
	else:
		print "Closing connection"
		conn.close()

if __name__ == "__main__":

	# Global variables
	# Welcome msg string
	WELCOME_MSG = ""
	# Server's ip address
	HOST = ""
	# Server's port number
	PORT = 0
	# THIS robot's name
	ROBOT_NAME = ""
	# THIS robots' status
	STATUS = ""
	# Buffer size for communication
	BUFFER_SIZE = 0

	main()
