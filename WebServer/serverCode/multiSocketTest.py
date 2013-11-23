import socket,thread,time

# Function to print data with time.
def printWithTime (data):
	print ("%s-->%s" % (time.asctime(), data))

# Function to send data
def sendData (sock, name):
	try:
		printWithTime ("%s started new thread" % name)
		for i in xrange(3):
			string = ("%s-%d:hi" % (name, i))
			printWithTime ("%s sending data:%s" % (name, string))
			sock.send (string)
	except socket.error, msg:
		printWithTime ('Socket error! Error code : %d. Error message : ' % msg[0], msg[1])
	except Exception as E:
		printWithTime ("Some exception! %s" % E)
	printWithTime ("Sending completed. Closing now")
	closeSocket (sock, name)


# Function to receive data
def receiveData (sock, name):
	while True:
		try:
			data = conn.recv(4096)
			if not data:
				break
			printWithTime ("%s received %s : " % name, data)
		except socket.error, msg:
			printWithTime ('Socket error! Error code : %d. Error message : ' % msg[0], msg[1])
	closeSocket (sock, name)

# Function to make a socket connection
def makeSocket(host, port):
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect ((host, port))
	return s

# Function to close a socket
def closeSocket (s,name):
	s.close()
	printWithTime ("%s closed." % name)

# Main function
def main () :
	host = "129.21.30.80"
	serverPort = 4000
	browserPort = 4010
	serverSocket = makeSocket(host,serverPort)
	browserSocket = makeSocket(host,browserPort)
	printWithTime ("Starting a new thread for server.")
	thread.start_new_thread (sendData, (serverSocket,"robot",))
	printWithTime ("Starting a new thread for browser.")
	thread.start_new_thread (sendData, (browserSocket,"browser",))
	# Forever loop.
	while (True):
		if not (threading.activeCount() > 1):
			break
	printWithTime ('Exiting!')

if __name__ == '__main__':
	main()