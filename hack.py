import sys
import socket
import itertools
import string
from urllib.request import urlopen


args = sys.argv
address = (str(args[1]), int(args[2]))

symbols = string.ascii_lowercase + string.digits

def brute_options():
    for i in range(len(symbols)):
        for combination in itertools.product(symbols, repeat=i + 1):
            yield ''.join(combination)


def file_options():
    url_file = urlopen('https://stepik.org/media/attachments/lesson/255258/passwords.txt').read()
    file = open('passwords.txt', 'w')
    file.write(url_file.decode())
    file.close()
    with open('passwords.txt') as file:
        for line in file.readlines():
            password = line.replace('\n', '')
            cases = [password]
            if not password.isdigit():
                for case in cases:
                    for n, letter in enumerate(case):
                        if letter.lower():
                            big_letter = letter.upper()
                            if n == 0:
                                new_password = big_letter + case[n + 1:]
                            elif n < len(password) - 1:
                                new_password = case[:n] + big_letter + case[n + 1:]
                            else:
                                new_password = case[:n] + big_letter
                            if new_password not in cases:
                                cases.append(new_password)
            for case in cases:
                yield case


with socket.socket() as server:
    server.connect(address)
    for option in file_options():
        server.send(option.encode())
        response = server.recv(1024).decode()
        if response == 'Connection success!':
            print(option)
            break
