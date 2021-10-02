    What do I need to get a functioning app?

    The server will transmit the data to the intended client.
    Server will handle each client connection, safely forming a connection.
    Any server opened on a private network will be accessed by all devices on that network.

    Port - 5000+
    Find a dead port above 5000 to be safe that isn't being used (typically above this number is safe)

    Server - Set an IP address (local) to run the server from.
    Is there a way to automatically grab an IP address so we can move the server from PC to PC?
    SERVER = socket.gethostbyname(socket.gethostname())
    Looks for the name of the host computer (grabs the local IP and the name that the PC is given, usually seen on a network map)

    Server socket will be set to IPv4 (AF_INET) and set to windows STREAM.
    Bind the server to the socket address.