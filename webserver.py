import os
import socket

from handler import Handler


class WebServer:
    workers = []

    def __init__(self, root_dir, ncpu, address, listeners, buff):
        self.root_dir = root_dir
        self.ncpu = ncpu
        self.address = address
        self.listeners = listeners
        self.buff = buff
        self.handler = Handler
        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen(self.listeners)
        for i in range(self.ncpu + 1):
            pid = os.fork()

            if pid != 0:
                self.workers.append(pid)
            else:
                print("Created worker on PID: {}".format(os.getpid()))
                while True:
                    client_socket, client_addr = self.server_socket.accept()
                    request = client_socket.recv(self.buff)
                    if len(request.strip()) == 0:
                        client_socket.close()
                        continue

                    response = self.handler.get_response(request)

                    client_socket.sendall(response)
                    client_socket.close()

        self.server_socket.close()

        for pid in self.workers:
            os.waitpid(pid, 0)
