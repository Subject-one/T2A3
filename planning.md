    What do I need to get a functioning app?

    ## File Transfer ##
    Client - the user who will receive the data. 
    *client to client isn't a safe connection model over the internet.
    Client will pass data to the server first. 

    The server will transmit the data to the intended client.
    Server will handle each client connection, safely forming a connection.
    Any server opened on a private network will be accessed by all devices on that network.

    Improving performance? - Threading
    Allows each part of code to run on individual threads isntead of waiting for other code to execute.
    https://docs.python.org/3/library/threading.html

    Port - 5000+
    Find a dead port above 5000 to be safe that isn't being used (typically above this number is safe)

    Server - Set an IP address (local) to run the server from.
    Is there a way to automatically grab an IP address so we can move the server from PC to PC?
    SERVER = socket.gethostbyname(socket.gethostname())
    Looks for the name of the host computer (grabs the local IP and the name that the PC is given, usually seen on a network map)

    Server socket will be set to IPv4 (AF_INET) and set to windows STREAM.
    Bind the server to the socket address.

    Progress bar - to know how the file process is progressing
    https://github.com/tqdm/tqdm
    OR
    write my own progress bar
    https://www.youtube.com/watch?v=iZnLZFRylbs&ab_channel=TomScott

    Do I need to deal with the OS?
    https://docs.python.org/3/library/os.html
    Mainly for clearing screens.

    Data log - instance attribute (possible class)
    To show what file name, time, size, time to transfer.

    Users class?

    Check out pickle?
