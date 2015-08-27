import socket
import threading

HOST = "localhost"
PORT = 9000
MAX_CLIENTS = 5
BUF_SIZE = 1024
DEFAULT_ENCODING = "utf-8"
connected_clients = []  # This will hold pairs of string and socket object.


def login(sock):
    username = "User" + str(len(connected_clients) + 1)
    num = len(connected_clients) + 1
    while islogged(username):  # While there's already an user with this name, change it.
        num += 1
        username = "User" + str(num)
    client = (username, sock)
    if client not in connected_clients:
        connected_clients.append(client)

    return username


def islogged(username):
    result = False
    for client in connected_clients:
        if client[0] == username:
            result = True
            break
    return result


def remove_client(usr):
    for client in connected_clients:
        if client[0] == usr:
            connected_clients.remove(client)


def handle(connection, address):
    if len(connected_clients) >= MAX_CLIENTS:
        connection.sendall("Server is full!".encode(DEFAULT_ENCODING))
        connection.close()
    else:
        username = login(connection)
        print("{} is connected at {}".format(username, address[0]))
        login_broadcast(username)
        try:
            while True:
                if len(connected_clients) < 2:
                    connection.sendall("You're alone right now. Wait for someone else to connect.")
                data = connection.recv(BUF_SIZE).decode(DEFAULT_ENCODING)
                if data == "":
                    print("Socket closed remotely for {}".format(username))
                    quit_broadcast(username)
                    break
                broadcast(username, data)
                print(">> {}: {}".format(username, data))
        except:
            print("Problem handling request from {}".format(username))
        finally:
            print("Closing socket for {}".format(username))
            connection.close()
            quit_broadcast(username)
            remove_client(username)


def broadcast(author, msg):  # Send a message to all connected clients
    for client in connected_clients:
        if client[0] != author:
            client[1].sendall((author + ": " + msg).encode(DEFAULT_ENCODING))


def quit_broadcast(user):  # Inform all other clients someone has left.
    for client in connected_clients:
        if client[0] != user:
            client[1].sendall(("SERVER: " + user + " disconnected.").encode(DEFAULT_ENCODING))


def login_broadcast(user):
    for client in connected_clients:
        if client[0] != user:
            client[1].sendall(("SERVER: " + user + " connected.").encode(DEFAULT_ENCODING))


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
