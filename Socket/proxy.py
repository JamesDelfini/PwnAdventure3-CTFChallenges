import socket
import ssl
import logging
import os
from threading import Thread

context = ssl.create_default_context()


class ServerLogic(Thread):
    def __init__(self, src_host, src_port, dst_host, dst_port) -> None:
        Thread.__init__(self)
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((self.src_host, self.src_port))
                    print("[*] Listening on port %i" % self.src_port)
                    s.listen(5)
                    self.conn, self.addr = s.accept()

                    with self.conn:
                        logging.info("[+] Connected %s:%i ==> %s:%i" %
                                     (self.addr[0], self.addr[1], self.src_host, self.src_port))
                        while True:
                            data = self.conn.recv(4096*4)

                            if not data:
                                break

                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                                s2.connect((self.dst_host, self.dst_port))
                                s2.sendall(data)
                                data2 = s2.recv(4096*4)

                                logging.debug(
                                    "[>>> Server >>>] %s" % data.hex())

                                logging.debug(
                                    "[<<<  Game  <<<] %s" % data2.hex())

                                self.conn.sendall(data2)

                    logging.info("[*] Closed %s:%i ==> %s:%i" %
                                 (self.addr[0], self.addr[1], self.src_host, self.src_port))
            except Exception as e:
                logging.error(e)


if __name__ == '__main__':
    # Logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    # master = ProxyServer("127.0.0.1", 65431, "127.0.0.1", 65432)
    # master.listen()

    # s = ServerLogic("127.0.0.1", 65431)
    # s.start()
    # print(s.wut)

    # src_host = "127.0.0.1"
    src_host = "0.0.0.0"
    dst_host = "192.168.1.9"

    server = ServerLogic(src_host, 3333, dst_host, 3333)
    server.start()

    # game = []
    # for i in range(5):
    #     _game = ServerLogic(src_host, 3000+i, dst_host, 3000+i)
    #     _game.start()
    #     game.append(_game)

    while True:
        try:
            cmd = input()
            if cmd[:1] == 'q':
                os._exit(0)
        except Exception as e:
            print(e)
