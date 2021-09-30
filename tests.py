import tqdm

class Message():
    def __init__(self, text: str):
        self.text = text.strip("b'")

    def __repr__(self) -> str:
        return self.text



# Set useful constants
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 6464
ADDRESS = SERVER, PORT
FORMAT = 'UTF-8'
BUFFER = 1024
SEPARATOR = "<SEPARATOR>"

# Address Family Internet, IPv4, TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ADDRESS))
server.listen(5)
print(f"[*] Server starting at: {SERVER}:{PORT}")

client_socket, address = server.accept() 
print(f"[+] {address} is connected.")


received = client_socket.recv(BUFFER).decode(FORMAT)
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)


progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER)
        if not bytes_read:    
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
server.close()





import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER = 1024
FORMAT = 'UTF-8'

# the ip address or hostname of the server, the receiver
host = "192.168.1.101"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "filename.dick"
# get the file size
filesize = os.path.getsize(filename)

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode(FORMAT))

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()