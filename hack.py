import sys
import socket
import itertools
import string

args = sys.argv
address = (str(args[1]), int(args[2]))

symbols = string.ascii_lowercase + string.digits


def options():
    for i in range(len(symbols)):
        for combination in itertools.product(symbols, repeat=i + 1):
            yield ''.join(combination)


with socket.socket() as client:
    client.connect(address)
    for option in options():
        client.send(option.encode())
        response = client.recv(1024).decode()
        if response == 'Connection success!':
            print(option)
            break

