import argparse
from webserver import WebServer

HOST = '127.0.0.1'
PORT = 80
NCPU = 2
BUFF = 1024
LISTENERS = 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('-r', type=str, help='root directory')
    parser.add_argument('-c', type=str, help='number of CPU')
    args = vars(parser.parse_args())

    NCPU = args['c'] or NCPU
    ROOT_DIR = args['r'] or ""
    ADDRESS = (HOST, PORT)

    webserver = WebServer(ROOT_DIR, NCPU, ADDRESS, LISTENERS, BUFF)
    webserver.start()