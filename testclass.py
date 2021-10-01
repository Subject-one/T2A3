import socket
import select
from datetime import datetime, timedelta

SERVER = '127.0.0.1'
PORT = 6050
ADDRESS = SERVER, PORT
HEADER = 10
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"



class Message:
    def __init__(self, text):
        self.text = text.decode(FORMAT).strip("b'")
        self.user, separator, self.message = self.text.partition(SEPARATOR)
        print(self.user)


    def __repr__(self) -> str:
        return self.user + ":" + self.message


class Server:
    def __init__(self, server="", port=6050):
        # Address Family Internet, IPv4, TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set, Set Attribute, Set Item True
        # Will allow users to reconnect to chat
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((server, port))
        self.active_sockets = [self.server_socket]
        self.users = {}
        print(f"Server has successfully launched on {SERVER}")
        print("=============================================")
        """Begins the setup process for a server.

        Sets the server to IPv4 TCP. 
        Will attempt to allow and users to reconnect.
        Bind to the ip and port given in initialise method.
        Holds any open actively connected connections.
        Creates a dictionary for users.

        Args:
            self: create the instance of the class.
            server: leaves an empty string for server IP to fill.
            port: sets the port to connect to.
        """


    def receive_msg(self, client_socket):
        try: 
            receive_header = client_socket.recv(HEADER)
            if not len(receive_header):
                return False
            msg_len = int(receive_header.decode(FORMAT).strip())
            return {"header": receive_header, "data": client_socket.recv(msg_len)}
        except:
            return False


    def comms(self):
        time = (datetime.now() + timedelta(hours=5)).strftime('%H:%M')
  
        while True:
            # Read list, write list and error list
            read_sockets, _, exception_sockets = select.select(self.active_sockets, [], self.active_sockets)

            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()

                    user = self.receive_msg(client_socket)
                    if user is False:
                        continue
                    print(user)

                    self.active_sockets.append(client_socket)
                    self.users[client_socket] = user
                    print(f"{user} has joined.")

                else:
                    message = self.receive_msg(notified_socket)
                    if message is False:
                        print(f"{user} has left.")
                        self.active_sockets.remove(notified_socket)
                        del self.users[notified_socket]
                        continue
                    user = self.users[notified_socket]
                    print(time)
                    print(Message(message['data']))

                    for client_socket in self.users:
                        print(self.users)
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                for notified_socket in exception_sockets:
                    self.active_sockets.remove(notified_socket)
                    del self.users[notified_socket]


    def start(self):
        self.server_socket.listen(5)
        # while True:
        #     conn, addr = server.accept()
            # thread = threading.Thread.__init__(args=(conn, addr))
            # thread.start()


server = Server(port=PORT)
server.start()
server.comms()