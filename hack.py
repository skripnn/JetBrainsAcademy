import sys
import socket


args = sys.argv
address = (str(args[1]), int(args[2]))
message = str(args[3])

with socket.socket() as sock:
    sock.connect(address)
    sock.send(message.encode())
    response = sock.recv(1024)
    print(response.decode())