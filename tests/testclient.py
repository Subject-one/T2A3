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
        try:
            self.set_username = input("Enter your username: ")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(ADDRESS)
            self.client_socket.setblocking(False)
            print("You are now connected to the server.")
            print(f"============={SERVER}==============")

            self.username = self.set_username.encode(FORMAT)
            self.username_header = f"{len(self.username):<{HEADER}}".encode(FORMAT)
            self.client_socket.send(self.username_header + self.username)

        except KeyboardInterrupt:
            self.destroy()


    def comms(self):
        while True:
            try:
                message = input(f"{self.set_username}: ")
                if message:
                    message = message.encode(FORMAT)
                    message = self.username + SEPARATOR + message 
                    message_header = f"{len(message):< {HEADER}}".encode(FORMAT)
                    self.client_socket.send(message_header + message)

            except KeyboardInterrupt:
                self.destroy(True)

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

            except BlockingIOError:
                pass

            except AttributeError:
                pass


    def destroy(self, conn=False):
        if conn:
            # Removes ^C by backspacing each time chr(8) is used.
            # Gets the character that represents the unicode 8.
            print(chr(8) + chr(8) + "Disconnecting from server..")
            self.send_msg(f"{self.username.decode(FORMAT).strip('b')} has left the server.")
            self.client_socket.shutdown(1)
            self.client_socket.close()
            sys.exit()
        else:
            print(chr(8) + chr(8) + "  ")
            print("Closing client...")
            sys.exit()


    def send_msg(self, message):
        message = message.encode(FORMAT)
        message = self.username + SEPARATOR + message 
        message_header = f"{len(message):< {HEADER}}".encode(FORMAT)
        self.client_socket.send(message_header + message)
        self.username



client = Client()
client.comms()