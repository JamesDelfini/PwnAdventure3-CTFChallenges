
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65431        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    for i in range(5):
        s.sendall(b'Hello, xxworld')
        s.settimeout(5.0)
        data = s.recv(1024)
        print('Received', repr(data))
