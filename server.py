"""
Runs the server thread
"""

import sys

from server_libs.server import Server

def server():
    if len(sys.argv) < 3:
        print ("Correct usage: Script, IP address, Port number")
        exit()

    ip_address =  sys.argv[1]
    port = int(sys.argv[2])
    server = Server(ip_address, port)
    server.run()


if __name__ == '__main__':
    server()