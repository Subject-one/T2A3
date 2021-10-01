import socket
from server import receive_msg
import sys

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 6464
ADDRESS = SERVER, PORT
HEADER = 10
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>".encode(FORMAT)

set_username = input("Enter a username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)
client_socket.setblocking(False)

username = set_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER}}".encode(FORMAT)
client_socket.send(username_header + username)


while True:
    message = input(f"{set_username} > ")
    if message:
        message = message.encode(FORMAT)
        message = username + SEPARATOR + message 
        message_header = f"{len(message):<{HEADER}}".encode(FORMAT)
        client_socket.send(message_header + message)

    try:
        while True:
            username_header = client_socket.recv(HEADER)
            if not len(username_header):
                print("Aborted Connection")
                sys.exit()

            username_length = int(username_length.decode(FORMAT).strip())
            username = client_socket.recv(username_length).decode(FORMAT)

            message_header = client_socket.recv(HEADER)
            message_length = int(message_header.decode(FORMAT).strip())
            message = client_socket.recv(username_length).decode(FORMAT)

            print(f"{username} > {message}")
    except:
        pass