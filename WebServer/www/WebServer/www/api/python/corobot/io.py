from asynchat import async_chat, simple_producer
import logging
import socket
import sys
from threading import Event, RLock

class LineClient(async_chat):
    """Sends line messages to the server and receives line responses."""

    def __init__(self, host, port, line_read):
        async_chat.__init__(self)
        self.line_read = line_read
        self.received_data = []
        self.set_terminator(b"\n")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def write_line(self, msg):
        self.producer_fifo.append(simple_producer(msg.encode("utf-8") + b"\n"))

    def collect_incoming_data(self, data):
        self.received_data.append(data)

    def found_terminator(self):
        line = ''.join(map(lambda b: b.decode("utf-8"), self.received_data))
        self.line_read(line)
        self.received_data = []

class CorobotClient(LineClient):

    def __init__(self, host, port, robot):
        LineClient.__init__(self, host, port, robot._robot_response)
        self.robot = robot

    def handle_connect(self):
        self.robot.connected_event.set()

    def handle_error(self):
        exc_type, exc, traceback = sys.exc_info()
        if self.connected:
            # Need to break out of blocking on any Future.wait() calls.
            for future in self.robot.futures.values():
                future._error_occured(exc)
        else:
            self.robot.error_connecting = True
            self.robot.connected_event.set()
        self.close_when_done()
