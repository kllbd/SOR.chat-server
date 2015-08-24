import socket

HOST = 'localhost'
PORT = 9000
MAX_CLIENTS = 5
BUF_SIZE = 1024
DEFAULT_ENCODING = 'ascii'

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = "some data"
    sock.sendall(data)
    result = sock.recv(BUF_SIZE)
    print(result)
    sock.close()
