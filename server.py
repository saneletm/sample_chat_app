"""
Runs the server thread
"""

from __future__ import absolute_import

import sys

from lib.server.server import Server


def server(address, port):
    serve = Server(address, port)
    serve.run()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Correct usage: Script, IP address, Port number")
        exit()

    server(sys.argv[1], int(sys.argv[2]))  # TODO: should check if argv[2] is digit
