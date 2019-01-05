"""
This is a server implementation of a chat app
This is only safe to use on the same machine (as in run both the server and client on the same machine)
Further cleanup would need to be done to support real clients on different machines (as of Jan 4 2019)
"""

import select
from multiprocessing import Event
from threading import Thread


class ClientThread(Thread):
    """
    For every connection the server receive, it will create an instance of a client thread to read from
    that conn, and enqueue msg to server inbox queue if it successfully reads from the connection,
    OW, send a msg signaling failure to read, which will clean up this thread and the connection obj
    """
    def __init__(self, conn, addr, msg_queue):
        Thread.__init__(self)
        self.addr = addr
        self.conn = conn
        self.msg_queue = msg_queue
        self.shutting_down_event = Event()

    def stop(self):
        """
        Signal for this client thead to stop
        """
        if not self.is_stopped():
            self.shutting_down_event.set()

    def is_stopped(self):
        """
        Checks if this client thread's signal to stop has been set
        """
        return self.shutting_down_event.is_set()

    def run(self):
        """
        Receive on the conn , and enqueue msg to server inbox queue 
        """

        try:
            self.conn.send("Welcome to this awesome chatroom!!!")
            hi = "<" + str(self.addr) + "> " + " says hi!"
            self.msg_queue.put((self.addr, hi))

            sent_bye = False
            select_timeout = 1

            while not self.shutting_down_event.is_set():
                # try to receive from conn
                try:
                    readable, _, _= select.select([self.conn], [], [], select_timeout)
                    if self.conn in readable:
                        message = self.conn.recv(2048)
                        # if you receive something confirmation message
                        msg_to_send = "<" + str(self.addr) + "> " + message if message else None
                        if not msg_to_send and not sent_bye:
                            # will send two msgs this time, a priliminary one to say goodby to our foos, the the empty to cleanup
                            bye = "<" + str(self.addr) + "> " + " says goodbye!"
                            self.msg_queue.put((self.addr, bye))
                            sent_bye = True  # need to have this flag since this can run for sometime before the thread stops
                            
                        self.msg_queue.put((self.addr, msg_to_send))
                except:  # Of cause this is not a good catch, and lint should complain
                    # Any exception... just continue, until some set count, then exit?
                    continue
        except KeyboardInterrupt:
            pass
        finally:
            # When all done, close socket and log exit
            # self.conn.close()  # TODO: verify server clean closes all socket conn objects
            print("{} client thread exited ".format(self.addr))
