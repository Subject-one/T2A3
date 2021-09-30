import socket
import threading
import sys

# Set constants
    # Define PORT. Numbers above 5000 are generally unused. 
PORT = 6060
    # Define SERVER GETHOSTNAME
    # Host name to IPv4, returns as string. (Doesn't work with IPv6)
SERVER = socket.gethostbyname(socket.gethostname())
    # Define Server, Port. Easy to bind a socket to a constant defined into a tuple
ADDRESS = (SERVER, PORT)
    # Set constant format 'utf-8'
FORMAT = 'UTF-8'
HANDLE = 1024
    # Define INET (Which socket to communicate to, IPv4, TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address
server.bind(ADDRESS)


class Server:
    def __init__(self, server="127.0.1.1", port=6050):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((server, port))
        


    def connect(conn, addr):
        connected = True
        while connected:
            message = conn.recv(HANDLE).decode(FORMAT)
            message = int(message)
            msg = conn.recv(message).decode(FORMAT)


    def start(self):
        self.server.listen(5)
        # while True:
        #     conn, addr = server.accept()
            # thread = threading.Thread.__init__(args=(conn, addr))
            # thread.start()

class Users:
    


my_server = Server()
my_server.start()
print(type(my_server.server))

            



        






        

# class Client:
#     def send(msg):
#         message = msg.encode(FORMAT)
#         msg_length = len(message)
#         send_length = str(msg_length).encode(FORMAT)
#         send_length += b' ' * (HEADER - len(send_length))
#         client.send(send_length)
#         client.send(message)
#         print(client.recv(2048).decode(FORMAT))





class Progress_Bar:
    pass

class Messaging:
    pass

class Error_Handling:
    pass
    # Try and Except for keyboard interrupt