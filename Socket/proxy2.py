import socket
import logging
import os
from importlib import reload
from threading import Thread
import parser_proxy


class ServerLogic(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.game = None
        self.host = host
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:
            data = self.server.recv(4096*4)

            if not data:
                break
            # if data:
            try:
                # logging.debug("[>>> Server >>>] %s" % data.hex())
                parser_proxy.parser(data, self.port, 'server')

                if (len(parser_proxy.CLIENT_QUEUE)) > 0:
                    pkt = parser_proxy.CLIENT_QUEUE.pop()
                    # print("got queue client: {}".format(pkt.hex()))
                    self.game.sendall(pkt)
            except Exception as err:
                logging.error(err)
                # raise

            # Forward in from server -> output to client
            self.game.sendall(data)

        # Close Connection
        # self.server.close()


class GameLogic(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.server = None
        self.host = host
        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

        logging.info("[*] Listening on port %i" % self.port)
        self.s.listen()
        self.game, self.addr = self.s.accept()

    def run(self):
        while True:
            if parser_proxy.CLOSE_CLIENT == self.port:
                print('Closed connection %i' % parser_proxy.CLOSE_CLIENT)

                # Close Connection
                # self.server.close()
                # self.game.close()
                self.s.close()

                # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # self.s.bind((self.host, self.port))

                # logging.info("[*] Listening on port %i" % self.port)
                # self.s.listen()
                # self.game, self.addr = self.s.accept()

                parser_proxy.CLOSE_CLIENT = 0
                # parser_proxy.CLIENT_CHANGE_LOC_INIT = False
                break

            data = self.game.recv(4096*4)

            if not data:
                break
            # if data:
            try:
                # logging.debug("[<<<  Game  <<<] %s" % data.hex())
                parser_proxy.parser(data, self.port, 'game')
                # print(len(parser_proxy.SERVER_QUEUE))

                if (len(parser_proxy.SERVER_QUEUE) > 0):
                    pkt = parser_proxy.SERVER_QUEUE.pop()
                    # print("got queue server: {}".format(pkt.hex()))
                    self.server.sendall(pkt)
            except Exception as err:
                logging.error(err)
                # raise

            # Forward in from client -> output to server
            self.server.sendall(data)

        # Close Connection
        # self.game.close()
        # self.s.close()


class Proxy(Thread):
    def __init__(self, src_host, src_port, dst_host, dst_port):
        Thread.__init__(self)
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.running = False

    def run(self):
        while True:
            try:
                self.gameLogic = GameLogic(self.src_host, self.src_port)
                self.serverLogic = ServerLogic(self.dst_host, self.dst_port)

                self.gameLogic.server = self.serverLogic.server
                self.serverLogic.game = self.gameLogic.game

                self.gameLogic.start()
                self.serverLogic.start()

                self.running = True
            except Exception as err:
                logging.error(err)
                # raise


if __name__ == '__main__':
    # Logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    src_host = "0.0.0.0"
    dst_host = "192.168.1.11"

    server = Proxy(src_host, 3333, dst_host, 3333)
    server.start()

    game_servers = []
    for i in range(5):
        _game = Proxy(src_host, 3000+i, dst_host, 3000+i)
        _game.start()
        game_servers.append(_game)

    while True:
        try:
            cmd = input()
            if cmd[:1] == 'q':
                os._exit(0)
            elif cmd[0:2] == 'S ':
                # send to server
                for server in game_servers:
                    if server.running:
                        parser_proxy.SERVER_QUEUE.append(
                            bytes.fromhex(cmd[2:]))
            elif cmd[0:2] == 'C ':
                # send to client
                for server in game_servers:
                    if server.running:
                        parser_proxy.CLIENT_QUEUE.append(
                            bytes.fromhex(cmd[2:]))
            else:
                reload(parser_proxy)
        except Exception as err:
            logging.error(err)
