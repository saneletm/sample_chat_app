import socket
import select
import sys
from multiprocessing import Event
from threading import Thread


class Client(Thread):
    def __init__(self, addr, port):
        self.address = addr
        self.port = port
        self.shutting_down = Event()

    def stop(self):
        """
        Sets shutting_down event signaling stop to the thread
        """

        if not self.is_stopped():
            self.shutting_down.set()

    def is_stopped(self):
        """
        Returns True if signal to stop this thread has been set
        """
        return self.shutting_down.is_set()

    def run(self):
        """
        Reads inport from either the connection from server, or from sys.stdin (user input)
        Display input from server
        Send input from stdin to server
        If input from server is '', stop and close --- server has gone away :(
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Running client on address: {}, port: {}".format(self.address, self.port)
            client.connect((self.address, self.port))
            streams = [sys.stdin, client]
            while not self.is_stopped():
                # select on streams
                read_sock, _, _= select.select(streams, [], [])
                # loop through read socket
                for sock in read_sock:
                    # if sock in read socks == server
                    if sock == client:
                        msg = sock.recv(2048)
                        if msg:
                            print "Message: ", msg
                        else:
                            print "Message: Server exited, Goodbye, have a nice day!"   # TODO: can server send this msg???
                            # NOTE:  finally statement will close connection
                            self.stop()
                    else:
                        msg = sys.stdin.readline()
                        client.send(msg)
                        sys.stdout.write("<You>")
                        sys.stdout.write(msg)
                        sys.stdout.flush()

        except KeyboardInterrupt:
            pass
        finally:
            client.close()
            print "Exiting client on address: {}, port {}".format(self.address, self.port)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Correct usage: Script, IP address, Port number")
        exit()
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    client = Client(ip_address, port)
    client.run()
