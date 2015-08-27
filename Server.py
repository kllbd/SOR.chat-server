import socket
import threading

HOST = "localhost"
PORT = 9000
MAX_CLIENTS = 5
BUF_SIZE = 1024
DEFAULT_ENCODING = "ascii"
clients = []  # This will hold pairs of string and socket object.


def login(sock):
    username = "User" + str(len(clients) + 1)
    num = len(clients) + 1
    while islogged(username):  # While there's already an user with this name, change it.
        num += 1
        username = "User" + str(num)
    client = (username, sock)
    if client not in clients:
        clients.append(client)

    return username


def islogged(username):
    result = False
    for client in clients:
        if client[0] == username:
            result = True
            break
    return result


def remove_client(usr):
    for client in clients:
        if client[0] == usr:
            clients.remove(client)


def handle(connection, address):
    if len(clients) >= MAX_CLIENTS:
        connection.sendall("Server is full!".encode(DEFAULT_ENCODING))
        connection.close()
    else:
        username = login(connection)
        print("{} is connected at {}".format(username, address[0]))
        broadcast("SERVER", username + " connected.")
        try:
            while True:
                data = connection.recv(BUF_SIZE).decode(DEFAULT_ENCODING)
                if data == "":
                    print("Socket closed remotely for {}".format(username))
                    broadcast("SERVER", username + " disconnected.")
                    break
                broadcast(username, data)
                print(">> {}: {}".format(username, data))
        except:
            print("Problem handling request from {}".format(username))
        finally:
            print("Closing socket for {}".format(username))
            connection.close()
            remove_client(username)


def broadcast(author, msg):  # Send a message to all connected clients
    for client in clients:
        if client[0] != author:
            client[1].sendall((author + ": " + msg).encode(DEFAULT_ENCODING))


class Server(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            print("New connection received. Starting thread to handle it.")
            process = threading.Thread(target=handle, args=(conn, address))
            process.start()
            print("New client being handled at thread: {}".format(process))

if __name__ == "__main__":
    server = Server(HOST, PORT)
    try:
        print("Server is active and listening to port {} at {}".format(str(server.port), server.hostname))
        server.start()
    except Exception as ex:
        print("Error: " + ex.__str__())
    finally:
        print("Shutting down")
