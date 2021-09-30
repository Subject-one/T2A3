import socket
import select


# Set useful constants
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 6464
ADDRESS = SERVER, PORT
HEADER = 10
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"

# Address Family Internet, IPv4, TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set, Set Attribute, Set Item True
# Will allow users to reconnect to chat
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDRESS)
server_socket.listen(5)

active_sockets = [server_socket]

# Use a dictionary to hold user information
users = {}

class Message():
    def __init__(self, text):
        self.text = text.decode(FORMAT).strip("b'")
        self.user, separator, self.message = self.text.partition(SEPARATOR)
        print(type(self.user))


    def __repr__(self) -> str:
        return self.user + ":" + self.message



def receive_msg(client_socket):
    try: 
        receive_header = client_socket.recv(HEADER)
        if not len(receive_header):
            return False
        msg_len = int(receive_header.decode(FORMAT).strip())
        return {"header": receive_header, "data": client_socket.recv(msg_len)}
    except:
        return False


while True:
    # Read list, write list and error list
    read_sockets, _, exception_sockets = select.select(active_sockets, [], active_sockets)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_msg(client_socket)
            if user is False:
                continue
            print(user)

            active_sockets.append(client_socket)
            users[client_socket] = user
            print(f"New Connection")

        else:
            message = receive_msg(notified_socket)
            if message is False:
                print("User left")
                active_sockets.remove(notified_socket)
                del users[notified_socket]
                continue
            user = users[notified_socket]
            print("Message")
            print(Message(message['data']))

            for client_socket in users:
                print(users)
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        for notified_socket in exception_sockets:
            active_sockets.remove(notified_socket)
            del users[notified_socket]


