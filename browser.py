import os
import sys
import requests
from bs4 import BeautifulSoup, SoupStrainer
from colorama import Fore, Back, Style


dir_name = ''
history = []
colour_start = '\033[34m'
colour_end = '\033[39m'


def beauty_soup(content):
    tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    only_tags = SoupStrainer(tags)
    soup = BeautifulSoup(content, 'html.parser', parse_only=only_tags)
    for each in soup.find_all('a'):
        if 'NavigableString' in str(type(each.string)):
            each.string = Fore.BLUE + each.string + Style.RESET_ALL
    return soup.get_text()


def create_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def history_add(line):
    history.append(line)
    line_input()


def line_input():
    line = input()
    if not check_command(line):
        check_URL(line)


def back():
    if len(history) > 1:
        history.pop()
        check_URL(history.pop())
    line_input()


def check_command(line):
    if line == 'exit':
        exit()
    elif line == 'back':
        back()
    else:
        return False


def add_https(url):
    if url.find('https://') == 0:
        return url
    elif url.find('http://') == 0:
        return url
    return 'https://' + url


def delete_https(url):
    if url.find('https://') == 0:
        return url[8:len(url)]
    elif url.find('http://') == 0:
        return url[7:len(url)]
    return url


def check_URL(url):
    last_dot_index = url.rfind('.')
    if last_dot_index == -1:
        check_file(url)
    else:
        open_page(add_https(url))


def open_page(url):
    request = requests.get(url)
    if request:
        #        print(request.text)
        #        print('\n\n\nБЬЮТИ:\n\n\n')
        beauty_request = beauty_soup(request.text)
        print(beauty_request)
        save_page(delete_https(url), beauty_request)
        history_add(url)
    else:
        print('Error: Page not found')
        line_input()


def save_page(url, page):
    file_name = get_file_name(url)
    with open(f'{dir_name}{file_name}', 'w') as f:
        f.write(page)


def open_saved_page(file_name):
    with open(f'{dir_name}{file_name}') as f:
        print(f.read())
    history_add(file_name)


def check_file(file_name):
    files = os.listdir(path=f'{dir_name}')
    if file_name in files:
        open_saved_page(file_name)
    else:
        print('Error: Incorrect URL')
        line_input()


def get_file_name(url):
    last_dot_index = url.rfind('.')
    return url[0:last_dot_index]


if len(sys.argv) > 1:
    create_dir(sys.argv[1])
    dir_name = sys.argv[1] + '/'


line_input()
