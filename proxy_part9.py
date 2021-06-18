import socket
import os
from threading import Thread
import parser_part9 as parser

# Part 9
# Developing a TCP Network Proxy - Pwn Adventure 3
# https://www.youtube.com/watch?v=iApNzWZG-10


class Proxy2Server(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.game = None  # game client socket not known yet
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    # run in thread
    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                print("[{}] <- {}".format(self.port, data[:100].hex()))
                # try:
                #     reload(parser)
                #     parser.parse(data, self.port, 'server')
                # except Exception as e:
                #     print("server[{}]".format(self.port), e)
                # forward to client
                self.game.sendall(data)


class Game2Proxy(Thread):

    def __init__(self, host, port):
        Thread.__init__(self)
        self.server = None  # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        self.game, addr = sock.accept()

    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                print("[{}] -> {}".format(self.port, data.hex()))
                # try:
                #     reload(parser)
                #     parser.parse(data, self.port, 'client')
                # except Exception as e:
                #     print "client[{}]".format(self.port), e
                # # forward to server
                self.server.sendall(data)


class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        Thread.__init__(self)
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while True:
            print("[proxy({})] setting up".format(self.port))
            # waiting for a client
            self.g2p = Game2Proxy(self.from_host, self.port)
            self.p2s = Proxy2Server(self.to_host, self.port)
            print("[proxy({})] connection established".format(self.port))
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game

            self.g2p.start()
            self.p2s.start()


master_server = Proxy('0.0.0.0', '192.168.1.9', 3333)
master_server.start()

game_servers = []
for port in range(3000, 3006):
    _game_server = Proxy('0.0.0.0', '192.168.1.9', port)
    _game_server.start()
    game_servers.append(_game_server)


while True:
    try:
        cmd = input('$ ')
        if cmd[:4] == 'quit':
            os._exit(0)
    except Exception as e:
        print(e)