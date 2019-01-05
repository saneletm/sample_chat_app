"""
Runs the server thread
"""

import sys

from lib.server.server import Server


def server(address, port):
    serve = Server(address, port)
    serve.run()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Correct usage: Script, IP address, Port number")
        exit()

    server(sys.argv[1], sys.argv[2])
