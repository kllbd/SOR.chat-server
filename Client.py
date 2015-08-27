import socket
import threading

HOST = 'localhost'
PORT = 9000
BUF_SIZE = 1024
DEFAULT_ENCODING = 'utf-8'
connected = False


def get_valid_msg():
    userinput = input()
    while len(userinput) > 64 or len(userinput) < 1:
        print("Message must be less than 64 characters and more than zero! Try again.")
        userinput = input()
    return userinput


def recv_from_server(conn, addr):
    global connected
    try:
        while len(data) > 1:
            data = conn.recv(BUF_SIZE).decode(DEFAULT_ENCODING)
            print(data)
        connected = False
    except:
        connected = False

if __name__ == "__main__":
    command = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    connected = True
    recv_thread = threading.Thread(target=recv_from_server, args=(sock, HOST))  # Start receive thread
    recv_thread.start()

    print("Connected!")
    try:
        while connected:
            msg = get_valid_msg()
            sock.sendall(msg.encode(DEFAULT_ENCODING))
        print("Exiting")
    except:
        connected = False
        print("Error. Exiting.")
