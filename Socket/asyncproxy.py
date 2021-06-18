import asyncore
import socket
import time
import errno


def parse(p_out):
    return p_out


class FixedDispatcher(asyncore.dispatcher):
    def handle_error(self):
        print("What happened?")
        raise

class Sock(FixedDispatcher):

    write_buffer = ""

    def readable(self):
        return not self.other.write_buffer

    def handle_read(self):
        self.other.write_buffer += self.recv(4096*4)

    def handle_write(self):
        if self.write_buffer:
            (p_in, p_out, p_next) = parse(self.write_buffer)
            self.other.write_buffer += p_in
            sent = self.send(p_out)
            self.write_buffer = self.write_buffer[sent:]
            self.write_buffer = p_next

    def handle_close(self):
        print(" [-] %i -> %i (closed)" %
              (self.getsockname()[1], self.getpeername()[1]))
        self.close()
        if self.other.other:
            self.other.close()
            self.other = None


class ProxServer(FixedDispatcher):
    def __init__(self, src_port, dst_host, dst_port):
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.client = None
        self.server = None
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("0.0.0.0", src_port))
        print(" [*] Listening on port %i" % src_port)
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()

        if not pair:
            return
        left, addr = pair

        try:
            right = socket.create_connection((self.dst_host, self.dst_port))
        except socket.error as e:
            if e.errno is not errno.ECONNREFUSED:
                raise
            print(" [!] Connection refused (%s:%i)" %
                  (self.dst_host, self.dst_port))
            left.close()
        else:
            print(" [+] %i:%i > %i:%i" %
                  (addr[1], self.src_port,
                   right.getsockname()[1], self.dst_port))

            self.client = Sock(left)
            self.server = Sock(right)

            self.client.other = self.server
            self.server.other = self.client

    def close(self):
        print(" [*] Closed %i ==> %i" %
              (self.src_port, self.dst_port))
        self.client.close()
        self.server.close()
        asyncore.dispatcher.close(self)


if __name__ == "__main__":
    host = "192.168.1.9"

    while True:
        # Change port here
        master = ProxServer(3333, host, 3333)
        game = ProxServer(3000, host, 3000)
        game2 = ProxServer(3001, host, 3001)
        game3 = ProxServer(3002, host, 3002)
        game4 = ProxServer(3003, host, 3003)
        game5 = ProxServer(3004, host, 3004)
        print("Proxy ready...")

        try:
            asyncore.loop()
        except Exception as e:
            print(e)

        master.close()
        game.close()
        game2.close()
        game3.close()
        game4.close()
        game5.close()

        time.sleep(0.5)
