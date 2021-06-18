import socket
import logging
import os
from threading import Thread
import time


class ProxyServer(Thread):
    def __init__(self, host, port) -> None:
        Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    logging.info(' [+] Connected by %s %i' %
                                 (addr[0], addr[1]))
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break

                        # time.sleep(3)
                        print(data)
                        conn.sendall(data)


if __name__ == '__main__':
    # Logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    proxy = ProxyServer("127.0.0.1", 65432)
    proxy.start()

    while True:
        try:
            cmd = input()
            if cmd[:1] == 'q':
                os._exit(0)
        except Exception as e:
            print(e)
