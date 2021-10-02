import socket
from sys import exit

SERVER = '127.0.0.1'
PORT = 6050
ADDRESS = SERVER, PORT
HEADER = 10
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>".encode(FORMAT)


class Client:
    def __init__(self):
        """Begins the process for connecting a client to the server.

        Asks for user input to setup a username.
        Sets the server to IPv4 TCP. 
        Send connection request.
        Set blocking or non-blocking mode of the socket: when false, the socket is set to non-blocking.
        Print notification to client that they connected.
        
        Username is set to encode to UTF-8.
        Username header is checked for length of header encoded to UTF-8.
        Client socket is sent with users information (header and username).

        Args:
            self: create the instance of the class.

        Except:
            Allows for user to CTRL-C out of program.
            Runs the destroy() method when called this way to handle KeyboardError.
        """
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
        """Handles client side outgoing communications.

        Starts a while loop that is set to True.
        Try: 
            Set a variable message that will take input from user.
            If input is True, runs send_msg() function with message.
    

        Try: 
            While loop True is set.
            Username header is set to client socket for received header constant.
            If length doesn't exist in username header:
            Print "Termination of connection" and exit the program.
            This happens when the server is shut down.
            The client side receives the notification and lets the client know this way.

        Args:
            self: create the instance of the class.

        Except:
            BlockingIOError is handled.
            It is raised when an operation would block an object, such as a socket.
            Setblocking is set to False which is why the exception is being handled.

            AttributeError.
            Raised when an attribute reference fails.

        """
        while True:
            try:
                message = input(f"{self.set_username}: ")
                if message:
                    self.send_msg(message)

            except KeyboardInterrupt:
                self.destroy(True)

            try:
                while True:
                    self.username_header = self.client_socket.recv(HEADER)
                    if not len(self.username_header):
                        print("Termination of connection")
                        exit()

            except BlockingIOError:
                pass

            except AttributeError:
                pass


    def destroy(self, conn=False):
        """Shuts down the server.

        conn is set to False.
        If conn is True (connection has been established):
        Print to client "Disconnecting from server.."

        Removes ^C by backspacing each time chr(8) is used.
        Gets the character that represents the unicode 8.

        Print to client "has left the server."
        Runs the shutdown method.
        Closes the socket.
        Exits the program.

        Args:
            self: creates an instance.
            conn: set to False by default.
            If it is set to False, it assumes there is no connection established unless True.
        """
        if conn:
            print(chr(8) + chr(8) + "Disconnecting from server..")
            self.send_msg(f"has left the server.")
            self.client_socket.shutdown(1)
            self.client_socket.close()
            exit()
        else:
            print(chr(8) + chr(8) + "  ")
            print("Closing client...")
            exit()


    def send_msg(self, message):
        """Prepares the client message for delivery to the server.

        Creates a variable message to encode data to UTF-8.
        Set the message to follow server rules using separator between name and message.
        Set a message header for outgoing confirmation, encoded to UTF-8.
        Send the data as client socket.

        Args:
            self: create the instance of the class.
            message: the message that the client will be sending to the server.

        Except:
            If any errors occur, returns False.
        """
        message = message.encode(FORMAT)
        message = self.username + SEPARATOR + message 
        message_header = f"{len(message):< {HEADER}}".encode(FORMAT)
        self.client_socket.send(message_header + message)
        self.username


client = Client()
client.comms()