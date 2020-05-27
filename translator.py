import requests
from bs4 import BeautifulSoup
from sys import argv

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
    lang_from = argv[1]
    lang_to = argv[2]
    if lang_to == 'all':
        lang_to = languages
        lang_to.remove(lang_from.capitalize())
    word = argv[3]
    # lang_from, lang_to, word = choose_languages()
    if type(lang_to) is list:
        file = f'{word}.txt'
        with open(file, 'w') as file:
            for language in lang_to:
                url = get_url(lang_from, language, word)
                html = get_response(url)
                words, phrases = parser(html)
                examples = make_examples(words, phrases, language, 1)
                print(examples)
                file.write(examples + '\n')

    else:
        url = get_url(lang_from, lang_to, word)
        html = get_response(url)
        words, phrases = parser(html)
        print_examples(words, phrases, lang_to, 5)


def choose_languages():
    print("Hello, you're welcome to the translator. Translator supports:")
    for n, language in enumerate(languages):
        print(f'{n + 1}. {language}')
    lang_from = input('Type the number of your language:\n')
    lang_from = languages[int(lang_from) - 1]
    lang_to = input("Type the number of language you want to translate to or '0' to translate to all languages:\n")
    if lang_to != '0':
        lang_to = languages[int(lang_to) - 1]
    else:
        lang_to = languages
        lang_to.remove(lang_from)
    word = input('Type the word you want to translate:\n').lower()
    return lang_from, lang_to, word


def make_examples(words, phrases, language, examples_number):
    examples = ''
    examples += f'{language} Translations:' + '\n'
    for n, i in enumerate(words):
        examples += i + '\n'
        if n == examples_number - 1:
            break
    examples += f'\n{language} Examples:' + '\n'
    for n, i in enumerate(phrases):
        if n % 2 == 0:
            examples += f'{i}:' + '\n'
        else:
            examples += f'{i}' + '\n\n'
            if n // 2 == examples_number - 1:
                break
    return examples


def print_examples(words, phrases, language, examples_number):
    print('\nContext examples:\n')
    print(make_examples(words, phrases, language, examples_number))


def get_response(url):
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})
    if response.status_code == 200:
        return response.text
    else:
        return None


def get_url(lang_from, lang_to, word):
    url = f'https://context.reverso.net/translation/{lang_from.lower()}-{lang_to.lower()}/{word}'
    return url


def parser(html):
    soup = BeautifulSoup(html, features="lxml")
    words_tags = ['a.translation.ltr.dict.first.n',
                  'a.translation.ltr.dict.no-pos',
                  'a.translation.rtl.dict.first.n',
                  'a.translation.rtl.dict.no-pos']
    words_part = soup.body.find(id='top-results')
    words_list = get_list_from_soup(words_part, words_tags)
    phrases_tags = ['div.src.ltr',
                    'div.trg.ltr',
                    'div.src.rtl',
                    'div.trg.rtl']
    phrases_part = soup.body.find(id='examples-content')
    phrases_list = get_list_from_soup(phrases_part, phrases_tags)
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
