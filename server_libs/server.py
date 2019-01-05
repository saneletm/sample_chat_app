"""
This is a server implementation of a chat app
This is only safe to use on the same machine (as in run both the server and client on the same machine)
Further cleanup would need to be done to support real clients on different machines (as of Jan 4 2019)
"""

import six
import select
import socket
import sys
import time
from collections import defaultdict
from multiprocessing import Event, Queue
from threading import Thread

from server_libs.client import ClientThread


class ConnStruct(object):
    """
    For every connection to the server... this will a pointer to the conn obj, the thread, and the addr tuple
    During cleanup/remove, make sure to close conn, and stop thread!
    Store instances of this in a map keyed by addr
    TODO: Make this a namedtuple from collections!!!!!!
    """
    def __init__(self, conn, client_thread):
        self.conn = conn
        self.thread = client_thread


class Server(object):
    """
    This thread will listen on the given addr/port and create an instance of client thread with 
    every connection it receive on accept
    This thread will have a inbox queue it will pass to all clients to send messages
    This thread will broadcast msgs received and cleanup client threads/connection objs that are 
    not responsive
    """
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port  = port
        self.shutting_down = Event()
        self.msg_queue = Queue()
        self.addr_to_conn_struct_map = {}

    def setup_for_run(self):
        """
        Sets up the server socket
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip_address, self.port))
        self.server.listen(100)
        self.server.setsockopt  
    
    def start_new_thread(self, conn, addr):
        """
        Creates a new client thread instance, and adds it to the map of known clients
        """
        thread = ClientThread(conn, addr, self.msg_queue)
        thread.start()
        return thread

    def broadcast(self, addr, message):
        """
        Sends  message to all clients/connections, except for the source connection/client
        """
        for  addr in set(six.iterkeys(self.addr_to_conn_struct_map)) - {addr}:
            try:
                self.addr_to_conn_struct_map[addr].conn.send(message)
            except:
                # if we have any error sending, close the client connection, then remove it from our list
                self.clean(addr)

    def clean(self, addr, keep=False):
        """
        Cleans connection artifacts, closing socket, stops thread, and remove entry from  instance map
        """
        if addr in six.iterkeys(self.addr_to_conn_struct_map):
            # close socket
            self.addr_to_conn_struct_map[addr].conn.close()
            # stop thread
            self.addr_to_conn_struct_map[addr].thread.stop()
            # remove struct from server map
            if not keep:  # TODO: total HACK : IF clean is called within a loop, and don't want to modify size of map?
                del self.addr_to_conn_struct_map[addr]

    def process_queue(self):
        """
        Empty server inbox queue and, broadcast msgs, or remove unresponsive client threads and conns
        """
        while not self.msg_queue.empty():
            addr, msg = self.msg_queue.get()
            if msg:
                print msg
                self.broadcast(addr, msg)
            else:
                self.clean(addr)

    def run(self):
        """
        Accept connection requests to the socket, creating client threads to service that conn
        Service inbox queue
        """

        print "Running server on address: {}, port: {}".format(self.ip_address, self.port)
        self.setup_for_run()

        try:
            read_list = [self.server]
            select_timeout = 1
            while True:
                # receive a connection request from client and get conn, addrr tuple
                readable, _, _= select.select(read_list, [], [], select_timeout)
                if self.server in readable:
                    conn, addr = self.server.accept()
                    # log connnection confirmation message
                    print addr[0] + " connected"
                    # start a new client thread with the new conn and address, and create  new struct
                    self.addr_to_conn_struct_map[addr] = ConnStruct(conn, self.start_new_thread(conn, addr))
                # process msgs in queue
                self.process_queue()

        except KeyboardInterrupt:
            pass
        finally:
            self.shutting_down.set()
            # wait for client threads to get the message and clean their sht
            print "Exiting Server Process, waiting for clients cleanup"

            for addr in self.addr_to_conn_struct_map:
                self.clean(addr, keep=True)
            time.sleep(1)
            self.server.close
            print "Done!"

