import socket

HOST = 'localhost'
PORT = 9000
BUF_SIZE = 1024
DEFAULT_ENCODING = 'ascii'

if __name__ == "__main__":
    command = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    while command != 'exit':
        command = input('Type your message: ')
        if command != 'exit':
            sock.sendall(command.encode(DEFAULT_ENCODING))
            result = sock.recv(BUF_SIZE)
            print(result.decode(DEFAULT_ENCODING))
    sock.close()
