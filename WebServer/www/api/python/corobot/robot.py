"""Python 3 user library for the Corobots project.

Z. Butler, Jan 2013
M. Bogue, April 2013

"""
import asyncore
from collections import deque
import os
from queue import Queue
import socket
from threading import Event, Lock, Thread

from corobot.common import CorobotException
from corobot.future import Future
from corobot.io import CorobotClient
from corobot.map import Map
import socket

class Robot():

    def __init__ (self):
        """Creates connection to robot."""
        self.next_msg_id = 1
        self.futures = {}
        self.out_lock = Lock()
        self.connected_event = Event()
        self.error_connecting = False
        #print ("In robot constructor. Fetching IP.")
        robotName, host = getIdleRobotIP()
        if (host is None):
            print ("Sorry, no IDLE corobot available.")
            raise CorobotException
        print ("Got IP as : %s" % str(host))
        print ("Robot assigned : %s" % robotName)
        port = 15001
        self.client = CorobotClient(host, port, self)
        self.io_thread = Thread(target=self._io_loop)
        self.io_thread.start()
        self.connected_event.wait()
        if self.error_connecting:
            raise CorobotException("Couldn't connect to robot at %s:%d" % (host, port))
        else:
            print ("Connected to corobot\n")
    def _io_loop(self):
        asyncore.loop(0.1)

    def _robot_response(self, msg):
        tokens = msg.split(" ")
        msg_id = int(tokens[0])
        key = tokens[1]
        data = tokens[2:]
        future = self.futures.pop(msg_id)
        if key == "POS":
            data = tuple(map(float, data))
        elif key == "CONFIRM":
            data = bool(data)
        elif key == "LOG":
            print(data)
            return
        else:
            data = None
        if key != "ERROR":
            future._fulfilled(data)
        else:
            future._error_occured(" ".join(data))

    def _write_message(self, msg):
        with self.out_lock:
            msg_id = self.next_msg_id
            self.next_msg_id += 1
            self.client.write_line("%d %s" % (msg_id, msg))
            future = Future()
            self.futures[msg_id] = future
            return future

    def nav_to(self, location):
        """Drives the robot to the given location with path planning."""
        print("Navigating to " + location + "\n")
        return self._write_message("NAVTOLOC " + location.upper())

    def nav_to_xy(self, x, y):
        """Drives the robot to the given location with path planning."""
        print("Navigating to position ("+x+", "+y+")\n")
        return self._write_message("NAVTOXY %f %f" % (x, y))

    def go_to(self, location):
        """Drives the robot in a straight line to the given location."""
        print("Going to " + location + "\n")
        return self._write_message("GOTOLOC " + location.upper())

    def go_to_xy(self, x, y):
        """Drives the robot in a straight line to the given coordinates."""
        print("Going to position ("+x+", "+y+")\n")
        return self._write_message("GOTOXY %f %f" % (x, y))

    def get_pos(self):
        """Returns the robot's position as an (x, y, theta) tuple."""
        print("Getting position\n")
        return self._write_message("GETPOS")

    def display_message(self, msg, timeout=120):
        """Requests the robot to display a message on its monitor."""
        print("Displaying message\n")
        return self._write_message("SHOW_MSG %d %s" % (timeout, msg))

    def request_confirm(self, msg, timeout=120):
        """Requests the robot to wait for confirmation from a local human."""
        print("Displaying confirmation\n")
        return self._write_message("SHOW_MSG_CONFIRM %d %s" % (timeout, msg))

    def get_closest_loc(self):
        """Returns the closest node to the current robot location."""
        raise NotImplementedError()

    def close(self):
        print("Closing connection\n")
        self.client.close_when_done()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
    
# Function to get IP of an idle robot from server process.
def getIdleRobotIP():
    """Function creates a socket connection to the server process and retrieves
        IP address of an IDLE robot.
        Returns : 1. If IDLE robot is found, returns its IP address.
                  2. Else returns None."""
    serverHostname = "vhost1.cs.rit.edu"
    serverPort = 65000
    try:
        robotSocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        robotSocket.connect ((serverHostname, serverPort))
        #robotIp = (robotSocket.recv (1024)).decode("UTF-8")
        data = (robotSocket.recv (1024)).decode("UTF-8")
        robotName, robotIp = data.split("-")
        if (robotIp == "None") or (robotIp == ""):
            robotIp = None
    except socket.error as E:
        print ("Socket error, while trying to retrieve connection information of IDLE robot from server.")
        print ("Error : %s" % str(E))
    finally:
        robotSocket.close()
        return robotName, robotIp
