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

class Robot():

    def __init__(self, host, port):
        """Creates connection to robot."""
        self.next_msg_id = 1
        self.futures = {}
        self.out_lock = Lock()
        self.connected_event = Event()
        self.error_connecting = False
        self.client = CorobotClient(host, port, self)
        self.io_thread = Thread(target=self._io_loop)
        self.io_thread.start()
        self.connected_event.wait()
        if self.error_connecting:
            raise CorobotException("Couldn't connect to robot at %s:%d" % (host, port))

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
        return self._write_message("NAVTOLOC " + location.upper())

    def nav_to_xy(self, x, y):
        """Drives the robot to the given location with path planning."""
        return self._write_message("NAVTOXY %f %f" % (x, y))

    def go_to(self, location):
        """Drives the robot in a straight line to the given location."""
        return self._write_message("GOTOLOC " + location.upper())

    def go_to_xy(self, x, y):
        """Drives the robot in a straight line to the given coordinates."""
        return self._write_message("GOTOXY %f %f" % (x, y))

    def get_pos(self):
        """Returns the robot's position as an (x, y, theta) tuple."""
        return self._write_message("GETPOS")

    def display_message(self, msg, timeout=120):
        """Requests the robot to display a message on its monitor."""
        return self._write_message("SHOW_MSG %d %s" % (timeout, msg))

    def request_confirm(self, msg, timeout=120):
        """Requests the robot to wait for confirmation from a local human."""
        return self._write_message("SHOW_MSG_CONFIRM %d %s" % (timeout, msg))

    def get_closest_loc(self):
        """Returns the closest node to the current robot location."""
        raise NotImplementedError()

    def close(self):
        self.client.close_when_done()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
