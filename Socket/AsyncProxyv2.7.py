# -*- coding: utf-8 -*-

import asyncore
import socket
import errno
import struct
import time


# Manipulate the data
def parse(p_out):
    # Identify generic spawn packet:
    # - 22 bytes long(always alone)
    # - 3rd and 4th = 0x00 (?? ??)
    # - Last 6 bytes = 0x00 (RR YY PP)

    if (len(p_out) == 22):
        print(p_out[2:4], p_out[16:])

    # if (len(p_out) == 22 and p_out[2:4] == "\x00\x00" and p_out[16:] == "\x00\x00\x00\x00\x00\x00"):
    if (len(p_out) == 22 and p_out[2:4] == "\x00\x00" and p_out[16:] == "\x00\x00\x00\x00\x00\x00"):
        packet_id = p_out[:2]  # We re-use the packet ID
        x = -39602.8
        y = -18288.0
        z = 2400.28 + 10000

        # Replace the spawn packet
        p_out = packet_id
        p_out += struct.pack("=HfffHHH", 0, x, y, z, 0, 0, 0)

    return p_out


class FixedDispatcher(asyncore.dispatcher):
    """https://docs.python.org/2/library/asyncore.html#asyncore.dispatcher"""

    def handle_error(self):
        print("What happened?")
        raise

# Buffer write_buffer for each TCP connection


class Sock(FixedDispatcher):
    write_buffer = b''

    # Called when the asynchronous loop detects that read()
    # call on the channel's socket will succeed
    def readable(self) -> bool:
        return not self.other.write_buffer

    # The data is parsed then copied in the buffer of the other connection
    def handle_read(self) -> None:
        self.other.write_buffer += self.recv(4096*4)

    def handle_write(self) -> None:
        if self.write_buffer:
            pkt = parse(self.write_buffer)
            sent = self.send(pkt)
            self.write_buffer = self.write_buffer[sent:]
        # if self.write_buffer:
            # (p_in, p_out, p_next) = parse(self.write_buffer)
            # # self.other.write_buffer += p_in
            # sent = self.send(p_out)
            # self.write_buffer = self.write_buffer[sent:]
            # self.write_buffer = p_next

    def handle_close(self):
        print(" [-] %i -> %i (closed)" %
              (self.getsockname()[1], self.getpeername()[1]))
        self.close()

        if self.other.other:
            self.other.close()
            self.other = None


class ProxServer(FixedDispatcher):
    def __init__(self, src_port, dst_host, dst_port) -> None:
        # Listener on port 3333
        self.src_port = src_port

        # Once client connected, create a new connection with server
        # To be process at handle_accept()
        self.dst_host = dst_host
        self.dst_port = dst_port

        self.client = None
        self.server = None

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('0.0.0.0', src_port))
        print(' [*] Listening on port %i' % src_port)
        self.listen(5)

    def handle_accept(self) -> None:
        pair = self.accept()

        if not pair:
            return

        left, addr = pair
        try:
            right = socket.create_connection((self.dst_host, self.dst_port))
        except socket.error as e:
            if e.errno is not errno.ECONNREFUSED:
                raise
            print(' [!] Connection refused (%s:%i)' %
                  (self.dst_host, self.dst_port))
            left.close()
        else:
            print(" [+] %i:%i > %i:%i" %
                  (addr[1], self.src_port,
                   right.getsockname()[1], self.dst_port))

            print('qs')
            self.client = Sock(left)
            self.server = Sock(right)

            # Forward input from client -> output to server
            self.client.other = self.server

            # Forward input from server -> output to client
            self.server.other = self.client

    def close(self) -> None:
        print(" [*] Closed %i ==> %i" %
              (self.src_port, self.dst_port))

        self.client.close()
        self.server.close()
        asyncore.dispatcher.close(self)


if __name__ == '__main__':
    while True:
        master = ProxServer(3333, '192.168.1.9', 3333)
        game1 = ProxServer(3000, '192.168.1.9', 3000)
        game2 = ProxServer(3001, '192.168.1.9', 3001)
        game3 = ProxServer(3002, '192.168.1.9', 3002)
        game4 = ProxServer(3003, '192.168.1.9', 3003)
        game5 = ProxServer(3004, '192.168.1.9', 3004)

        print("Proxy ready...")

        try:
            asyncore.loop()
        except Exception as e:
            print(e)

        master.close()
        game1.close()
        game2.close()
        game3.close()
        game4.close()
        game5.close()

        time.sleep(0.5)
