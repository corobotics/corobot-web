import socket,sys,thread,traceback,time

# Function to handle communication with clients
def clientThread(conn):
	
	""" Continuously receive the data - robot's status. Breaking condition -
	if no data received in '5' seconds - declare robot as 'dead'."""
	while True:
		data = conn.recv (BUFFER_SIZE)
		if not data:
			break
		print "Data received - " + data
		conn.send ("\nOK...")

# Main function
def main():

	"""
	1. Creates a socket for communication with the clients (robots).
	2. After accepting a call, communicates with the client on a separate
		port."""

	# Creating a communication socket
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # 0. Bind the socket
        try:
                s.bind((HOST,PORT))
                print "Socket binded successfully"

                # 0. Listen for incoming connections
                print "Waiting for connection at port - " + str(PORT)
                s.listen(MAX_NO_OF_CONNECTIONS)

                # 1. Wait for incoming connections
                while True:
                        """ accept() blocks the call - returns a new socket 
			object and address of the client."""

                        try:
                                conn,addr = s.accept()
                                ip,new_port = addr
				t = time.asctime(time.localtime(time.time()))
				print t,
                                print "Connected to : " + ip + " at port : " \
				+ str(new_port)

				conn.send (WELCOME_MSG)
				text = "Your ip is : " + ip
				# Send data 5 times
				for i in xrange(5):
					conn.send (text + ":" + str(i))
					time.sleep(1)

				# Start new thread
		                """thread.start_new_thread (clientThread,
						 (conn,))"""
				conn.send("Closing connection")
				conn.close()
				print ("Connection to %s closed.") %ip
				
			
			# In case of any exception, do not spawn a new thread
			except Exception, msg:
				print "Exception while communicating with"\
					" %s. Closing connection." %(str(ip))
				conn.close()
				print "Error Message : %s" %msg
				print "More info : " + str(sys.exc_info()[2])

        except socket.error, msg:
                print "Sock error! Error-code : " + str(msg[0]) + ".Error-msg :"\
			+ str(msg[1])
                sys.exit()

        finally:
                s.close()

if __name__ == "__main__":

	WELCOME_MSG="Welcome to corobotics app server."
	HOST=""
	PORT=8090
	BUFFER_SIZE = 4096
	MAX_NO_OF_CONNECTIONS=10
	ROBOTS_INFO_DICT = {}

	print "\t%s" % WELCOME_MSG

	main()
