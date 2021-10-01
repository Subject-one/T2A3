import socket
import sys

SERVER = '127.0.0.1'
PORT = 6050
ADDRESS = SERVER, PORT
HEADER = 10
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>".encode(FORMAT)


class Client:
    def __init__(self):
        self.set_username = input("Enter your username: ")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDRESS)
        self.client_socket.setblocking(False)

        self.username = self.set_username.encode(FORMAT)
        self.username_header = f"{len(self.username):<{HEADER}}".encode(FORMAT)
        self.client_socket.send(self.username_header + self.username)


    def comms(self):
        while True:
            message = input(f"{self.set_username}: ")
            if message:
                message = message.encode(FORMAT)
                message = self.username + SEPARATOR + message 
                message_header = f"{len(message):< {HEADER}}".encode(FORMAT)
                self.client_socket.send(message_header + message)

            try:
                while True:
                    self.username_header = self.client_socket.recv(HEADER)
                    if not len(self.username_header):
                        print("Aborted Connection")
                        sys.exit()

                    self.username_length = int(self.username_length.decode(FORMAT).strip())
                    self.username = self.client_socket.recv(self.username_length).decode(FORMAT)

                    self.message_header = self.client_socket.recv(HEADER)
                    self.message_length = int(self.message_header.decode(FORMAT).strip())
                    message = self.client_socket.recv(self.username_length).decode(FORMAT)

                    print(f"{self.username} > {message}")
            except:
                pass

client = Client()
client.comms()