from __future__ import absolute_import

import sys

from lib.client import Client


def client(address, port):
    serve = Client(address, port)
    serve.run()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Correct usage: Script, IP address, Port number")
        exit()

    client(sys.argv[1], int(sys.argv[2]))
