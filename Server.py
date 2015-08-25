import multiprocessing
import socket

HOST = "localhost"
PORT = 9000
MAX_CLIENTS = 5
BUF_SIZE = 1024
DEFAULT_ENCODING = "ascii"
clients = []


def handle(connection, address):
    if len(clients) >= MAX_CLIENTS:
        connection.sendall("Server is full!".encode(DEFAULT_ENCODING))
        connection.close()
    else:
        username = "User" + str(len(clients) + 1)
        clients.append(username)
        try:
            print("{} is connected at {}".format(username, address[0]))
            while True:
                data = connection.recv(BUF_SIZE).decode(DEFAULT_ENCODING)
                if data == "":
                    print("Socket closed remotely for {}".format(username))
                    break
                print("{}: {}".format(username, data))
        except:
            print("Problem handling request from {}".format(username))
        finally:
            print("Closing socket for {}".format(username))
            connection.close()


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
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            print("New client being handled at process {}".format(process))

if __name__ == "__main__":
    server = Server(HOST, PORT)
    try:
        print("Listening to port {} at {}".format(str(server.port), server.hostname))
        server.start()
    except Exception as ex:
        print("Error: " + ex.__str__())
    finally:
        print("Shutting down")
        for process in multiprocessing.active_children():
            print("Shutting down process {}".format(process))
            process.terminate()
            process.join()
    print("All done")
