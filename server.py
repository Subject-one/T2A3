import socket
import select
from datetime import datetime, timedelta
from sys import exit


SERVER = '127.0.0.1'
PORT = 6050
ADDRESS = SERVER, PORT
HEADER = 10
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"


class Message:
    def __init__(self, text):
        """Initialises for message format.

        init method is called.
        Takes the text from and removes the b'(bytes literal) after decoding to UTF-8.
        Sets the separator between the users name and the message sent.

        Args:
            self: create the instance of the class.
            text: where the text will be used.
        """
        self.text = text.decode(FORMAT).strip("b'")
        self.user, separator, self.message = self.text.partition(SEPARATOR)


    def __repr__(self) -> str:
        """Initialises for message format.

        repr method is called to to represent the incoming data.
        Add ": " to the end of the users name.
        Adds the message after.
        This format is followed for all incoming messages
        from clients.

        Args:
            self: create the instance of the class.
        """
        return self.user + ": " + self.message



class Server:
    def __init__(self, server="", port=6050):
        """Begins the setup process for a server.

        Sets the server to IPv4 TCP. 
        Will attempt to allow and users to reconnect.
        Bind to the ip and port given in initialise method.
        Holds any open actively connected connections.
        Creates a dictionary for users.
        Prints a message to the server to let admin know its successfully running.

        Args:
            self: create the instance of the class.
            server: leaves an empty string for server IP to fill.
            port: sets the port to connect to.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((server, port))
        self.active_sockets = [self.server_socket]
        self.users = {}
        print(f"Server has successfully launched on {SERVER}")
        print("=============================================")



    def receive_msg(self, client_socket):
        """Uses recv to receive incoming messages from clients.

        The function will attempt to receive a message header from the client.
        If the client connection can't be established returns False.
        Set the msg_len variable to be an integer and decode to UTF-8, stripping the ends.
        returns the received header and client socket as a dictionary.

        Args:
            self: create the instance of the class.
            client_socket: the client attempting to connect to the server.

        Except:
            If any errors occur, returns False.
        """
        try: 
            receive_header = client_socket.recv(HEADER)
            if not len(receive_header):
                return False
            msg_len = int(receive_header.decode(FORMAT).strip())
            return {"header": receive_header, "data": client_socket.recv(msg_len)}
        except:
                return False


    # Will remove the b' from text after it is decoded.
    def join_msg_strip(self, text):
        text = text.decode(FORMAT).strip("b'")
        return text


    def comms(self):
        """Main body of controlling the servers incoming messages, connections
           and how to manage them.

        Sets a variable to manage the time with the module datetime.
        Enters a while Loop that is set to True.
        Try execute to read sockets in active sockets list.
        For loop begins. Will accept the connection if the client socket is found
        in the server socket list.
        Attempts to read the client message.
        Appends the active socket from client  to the client socket list.
        Print a message with the join_msg_strip function to announce in server
        that the user has joined.

        Set variable message to receive_msg from the client socket.
        Set users dictionary with access to the client socket to be user.
        Remove the active socket from the notified sockets list.
        Set the user to the users dictionary notified socket.
        Print the time variable.
        Print the users message, accessing index data from the dictionary.

        Args:
            self: create the instance of the class.
        """
        time = (datetime.now() + timedelta(hours=5)).strftime('%H:%M')
        
        while True:
            try:
            # Read list, write list and error list
                read_sockets, _, exception_sockets = select.select(self.active_sockets, [], self.active_sockets)

                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        user = self.receive_msg(client_socket)
                        if user is False:
                            continue

                        self.active_sockets.append(client_socket)
                        self.users[client_socket] = user
                        print(f"{self.join_msg_strip(user['data'])} has joined.")

                    else:
                        message = self.receive_msg(notified_socket)
                        if message is False:
                            self.active_sockets.remove(notified_socket)
                            del self.users[notified_socket]
                            continue
                        user = self.users[notified_socket]
                        print(time)
                        print(Message(message['data']))

            except KeyboardInterrupt:
                self.destroy()


    def start(self):
        # Starts listening for incoming connections
        self.server_socket.listen(5)


    def destroy(self):
        """Shuts down the server.

        Runs the shutdown method.
        Removes ^C by backspacing each time chr(8) is used.
        Gets the character that represents the unicode 8.
        Closes the socket.
        Exits the program.

        Args:
            self: creates an instance.
        """
        self.server_socket.shutdown(1)
        print(chr(8) + chr(8) + "Server is shutting down...")
        self.server_socket.close()
        exit()



server = Server(port=PORT)
server.start()
server.comms()