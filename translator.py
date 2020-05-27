import requests
from bs4 import BeautifulSoup

languages = ['Arabic',
             'German',
             'English',
             'Spanish',
             'French',
             'Hebrew',
             'Japanese',
             'Dutch',
             'Polish',
             'Portuguese',
             'Romanian',
             'Russian',
             'Turkish'
             ]


def start():
    lang_from, lang_to, word = choose_languages()
    url = get_url(lang_from, lang_to, word)
    html = get_response(url)
    if html is None:
        exit()
    words, phrases = parser(html)
    print_examples(words, phrases, lang_to)


def choose_languages():
    print("Hello, you're welcome to the translator. Translator supports:")
    for n, language in enumerate(languages):
        print(f'{n + 1}. {language}')
    lang_from = input('Type the number of your language:\n')
    lang_from = languages[int(lang_from) - 1]
    lang_to = input('Type the number of language you want to translate to:\n')
    lang_to = languages[int(lang_to) - 1]
    word = input('Type the word you want to translate:\n')
    return lang_from, lang_to, word


def print_examples(words, phrases, language):
    print('\nContext examples:')
    print(f'\n{language} Translations:')
    for n, i in enumerate(words):
        print(i)
        if n == 4:
            break
    print(f'\n{language} Examples:')
    for n, i in enumerate(phrases):
        if n % 2 == 0:
            print(f'{i}:')
        else:
            print(f'{i}')
            if n // 2 == 4:
                break
            print('')


# def input_params():
#     language = input(
#         'Type "en" if you want to translate from French into English, '
#         'or "fr" if you want to translate from English into French:\n')
#     word = input('Type the word you want to translate:\n')
#     print(f'You chose "{language}" as the language to translate "{word}" to.')
#     return language, word


def get_response(url):
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})
    if response.status_code == 200:
        print(response.status_code, 'OK')
        return response.text
    else:
        print(response.status_code)
        return None


def get_url(lang_from, lang_to, word):
    url = f'https://context.reverso.net/translation/{lang_from.lower()}-{lang_to.lower()}/{word}'
    return url


def parser(html):
    soup = BeautifulSoup(html, features="lxml")
    words_tags = ['a.translation.ltr.dict.first.n', 'a.translation.ltr.dict.no-pos']
    words_list = get_list_from_soup(soup, words_tags)
    phrases_tags = ['div.src.ltr', 'div.trg.ltr']
    phrases_list = get_list_from_soup(soup, phrases_tags)
    return words_list, phrases_list


def get_list_from_soup(soup, tags):
    result = soup.select(', '.join(tags))
    result_list = []
    for i in result:
        soup_ = BeautifulSoup(str(i), features="lxml")
        phrase = soup_.get_text()
        result_list.append(phrase.strip())
    return result_list


start()
