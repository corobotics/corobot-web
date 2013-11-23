import socket, sys, time, threading

# My threading class
class MyThread (threading.Thread):
	def __init__ (self, conn):
		threading.Thread.__init__ (self)
		self.conn = conn

	def setConn (self, conn):
		self.conn = conn

	def run(self):
		statusList = ("BUSY", "IDLE")
		i = 0
		count = 0
		try:
			while count < 10:
				print ("Sending %d of 10" % (count+1))
				self.conn.send(ROBOT_NAME + ":" + statusList[i]+"\n\r")
				# Sleep for 1 second
				time.sleep(1)
				i += 1
				if i > 1:
					i=0
				count += 1
		except socket.error, msg:
			print "Error while sending data. Error message : %s" %(msg)

# Usage function
def usage():
	"""Function displays the usage for this program"""
	print "USAGE : python robot.py <robot-name> <port> ['<debug>']"
	sys.exit(1)

# Function to initialize with default values
def init (WELCOME_MSG="", HOST="", PORT=0, ROBOT_NAME="", STATUS="",
		BUFFER_SIZE=0):
	"""
	Includes variables for the default communication setup.
	If any of the parameters are not defined, use the mentioned default 
	ones"""

	if WELCOME_MSG == "" :
		WELCOME_MSG = "Welcome to corobotics server."
	if HOST == "":
		HOST = "129.21.30.80"
	"""if PORT == 0:
		PORT = 51000 
	if ROBOT_NAME == '':
		ROBOT_NAME = 'Robot 1'"""
	if STATUS == "":
		STATUS = "IDLE"
	if BUFFER_SIZE == 0:
		BUFFER_SIZE = 4096
	
	globals()["WELCOME_MSG"] = WELCOME_MSG
	globals()["HOST"] = HOST
	if PORT != 0:
		globals()["PORT"] = PORT
	if ROBOT_NAME != "":
		globals()["ROBOT_NAME"] = ROBOT_NAME
	globals()["STATUS"] = STATUS
	globals()["BUFFER_SIZE"] = BUFFER_SIZE
	
	# DEBUG 
	if DEBUG:
		print "Initialized with -->\nWELCOME_MSG : %s\nHOST : %s\n" \
		"PORT : %s\nROBOT_NAME : %s\nSTATUS : %s\nBUFFER_SIZE : %s" \
		% (WELCOME_MSG, HOST,PORT,ROBOT_NAME,STATUS,BUFFER_SIZE)

""" Function to communicate with the server. Continuously send the status to the 
server."""
def communicate (conn):
	statusList = ("BUSY", "IDLE")
	i = 0
	count = 0
	try:
		while count < 10:
			print ("Sending %d of 10" % (count+1))
			conn.send(ROBOT_NAME + ":" + statusList[i]+"\n\r")
			# Sleep for 1 second
			time.sleep(1)
			i += 1
			if i > 1:
				i=0
			count += 1
	except socket.error, msg:
		print "Error while sending data. Error message : %s" %(msg)

# Main function
def main ():
	
	# Set the default values
	init()
	
	print "\t---%s TERMINAL---" % (ROBOT_NAME)
	print "Debug status : %s" % str(DEBUG)
	
	# Create a communicating socket
	try:
	    #create an AF_INET, STREAM socket (TCP)
	    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "Failed to create socket. Error code: %s , Error message : " \
	    	% (str(msg[0]), msg[1])
		sys.exit()
	
	if DEBUG: 
		print "Socket Created"
	
	# 2. Communicate with remote server - HANDSHAKE
	try:
		conn.connect((HOST , PORT)) 
		if DEBUG:
			print "Socket connected to %s  at port : %s" \
				% (HOST, str(PORT))

		# Blocking call
		data = conn.recv (BUFFER_SIZE)
		print "Data received : %s" %(data)
		print "Required : %s" %(WELCOME_MSG)
		if data == WELCOME_MSG:
			# Connection was successful
			print "Successful handshake"
			message = ROBOT_NAME + ":" + STATUS
	    
		    # 3. Send the robot name and initial status
		   	print "Sending message : %s" % message
		   	conn.sendall(message)
			print "Message sent : %s" %message

			# 4. Now continuously communicate with server.
			#communicate (conn)
			new_thread = MyThread(conn)
			new_thread.start()
			print ("Main thread closed now.")
			
		else:
			print ("Incorrect data received from server.\nData : %s " %(data))
	except socket.error,message:
		print message
		print "Closing socket"
		conn.close()
	except Exception, msg:
		print "Exception. More messages : %s" % msg
		conn.close()
	
	else:
		print "Closing connection"
		# Wait for new_thread to close.
		new_thread.join()
		# Close connection.
		conn.close()

if __name__ == "__main__":

	if (len (sys.argv) < 3):
		usage()
	
	# Global variables
	# Welcome msg string
	WELCOME_MSG = ""
	# Server's ip address
	HOST = ""
	# Server's port number
	PORT = int (sys.argv[2])
	# THIS robot's name
	ROBOT_NAME = sys.argv[1]
	# THIS robots' status
	STATUS = ""
	# Buffer size for communication
	BUFFER_SIZE = 0
	
	# Debug flag to print diagnostics
	DEBUG = False
	
	# Debug option provided
	if (len(sys.argv) > 3) and sys.argv[3].lower() == "debug":
		DEBUG = True
	
	main()
