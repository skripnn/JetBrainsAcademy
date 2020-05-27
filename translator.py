import requests
from bs4 import BeautifulSoup
import lxml


def start():
    language, word = input_params()
    url = get_url(language, word)
    html = get_response(url)
    parser(html)


def input_params():
    language = input(
        'Type "en" if you want to translate from French into English, '
        'or "fr" if you want to translate from English into French:\n')
    word = input('Type the word you want to translate:\n')
    print(f'You chose "{language}" as the language to translate "{word}" to.')
    return language, word


def get_response(url):
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})
    if response.status_code == 200:
        print(response.status_code, 'OK')
    else:
        print(response.status_code)
    return response.text


def get_url(language, word):
    if language == 'fr':
        lang = 'english-french'
    elif language == 'en':
        lang = 'french-english'
    else:
        return None
    url = f"https://context.reverso.net/translation/{lang}/{word}"
    return url


def parser(html):
    soup = BeautifulSoup(html, features="lxml")
    words_tags = ['a.translation.ltr.dict.first.n', 'a.translation.ltr.dict.no-pos']
    words_list = get_list_from_soup(soup, words_tags)
    phrases_tags = ['div.src.ltr', 'div.trg.ltr']
    phrases_list = get_list_from_soup(soup, phrases_tags)
    words = ', '.join(words_list)
    phrases = ', '.join(phrases_list)
    print('Translation, ' + words)
    print('Translation, ' + phrases)


def get_list_from_soup(soup, tags):
    result = soup.select(', '.join(tags))
    result_list = []
    for i in result:
        soup_ = BeautifulSoup(str(i), features="lxml")
        phrase = soup_.get_text()
        result_list.append(phrase.strip())
    return result_list




start()