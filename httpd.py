import argparse
import os

from webserver import WebServer

HOST = '127.0.0.1'
PORT = 80
NCPU = os.cpu_count()
BUFF = 1024
LISTENERS = 1000
ROOT_DIR = "/home/timur/"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('-r', type=str, help='root directory')
    parser.add_argument('-c', type=int, help='number of CPU')
    args = vars(parser.parse_args())

    ncpu = args['c'] or NCPU
    root_dir = args['r'] or ROOT_DIR
    address = (HOST, PORT)

    webserver = WebServer(root_dir, ncpu, address, LISTENERS, BUFF)
    webserver.start()