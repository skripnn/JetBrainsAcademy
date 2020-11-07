import random
import io
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--export_to')
parser.add_argument('--import_from')
args = parser.parse_args()

log = io.StringIO()


def my_input():
    string = input()
    log.write(string + '\n')
    return string


def my_print(string, **kwargs):
    print(string, **kwargs)
    log.write(string + '\n')


class Card:
    cards = []

    def __init__(self, term=None, definition=None, mistakes=0):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes

    def reset_mistakes(self):
        for card in self.cards:
            card.mistakes = 0
        my_print('Card statistics has been reset.')

    def create(self):
        self.cards.append(self)

    def add(self):
        my_print(f'The card:')
        term = my_input()
        while term in self.terms():
            my_print(f'The term "{term}" already exists. Try again:')
            term = my_input()
        self.term = term
        my_print(f'The definition of the card:')
        definition = my_input()
        while definition in self.definitions():
            my_print(f'The definition "{definition}" already exists. Try again:')
            definition = my_input()
        self.definition = definition
        self.create()
        my_print(f'The pair ("{self.term}":"{self.definition}") has been added.')

    def remove(self):
        my_print(f'Which card?:')
        term = my_input()
        for card in self.cards:
            if card.term == term:
                Card.cards.remove(card)
                my_print('The card has been removed.')
        my_print(f'Can\'t remove "{term}": there is no such card.')

    def answer(self, definition):
        if definition == self.definition:
            my_print('Correct!')
        else:
            my_print(f'Wrong. The right answer is "{self.definition}"', end='')
            self.mistakes += 1
            card = Card(definition=definition).get()
            if card is not None:
                my_print(f', but your definition is correct for "{card.term}"', end='')
            my_print('.')

    def question(self):
        my_print(f'Print the definition of "{self.term}":')
        self.answer(my_input())

    def definitions(self):
        return [card.definition for card in self.cards]

    def terms(self):
        return [card.term for card in self.cards]

    def get(self):
        for card in self.cards:
            if card.term == self.term or card.definition == self.definition:
                return card
        return None


class Menu:
    def __init__(self):
        if args.import_from is not None:
            self.do_import(args.import_from)
        while True:
            self.input()

    def input(self):
        my_print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        action = my_input()
        exec('self.do_' + action.replace(' ', '_') + '()')
        my_print('')

    def do_log(self):
        my_print('File name:')
        file_name = my_input()
        file = open(file_name, "w", encoding="utf-8")
        file.write(log.getvalue())
        file.close()
        my_print('The log has been saved.')

    def do_reset_stats(self):
        Card().reset_mistakes()

    def do_hardest_card(self):
        sort_cards = sorted(Card.cards, key=lambda card: card.mistakes, reverse=True)
        if len(sort_cards) == 0 or sort_cards[0].mistakes == 0:
            my_print('There are no cards with errors.')
        else:
            max_mistakes = sort_cards[0].mistakes
            hardest_cards = [card.term for card in Card.cards if card.mistakes == max_mistakes]
            s = 's are'
            if len(hardest_cards) == 1:
                s = ' is'
            my_print(
                f'The hardest card{s} "{", ".join(hardest_cards)}". You have {max_mistakes} errors answering it.')

    def do_add(self):
        Card().add()

    def do_remove(self):
        Card().remove()

    def do_ask(self):
        my_print('How many times to ask?')
        n = int(my_input())
        for _ in range(n):
            i = random.randint(0, len(Card.cards) - 1)
            card = Card.cards[i]
            card.question()

    def do_exit(self):
        my_print('Bye bye!')
        if args.export_to is not None:
            self.do_export(args.export_to)
        exit()

    def do_export(self, file_name=None):
        if file_name is None:
            my_print('File name:')
            file_name = my_input()
        file = open(file_name, 'w')
        for card in Card.cards:
            file.write(card.term + '|' + card.definition + '|' + str(card.mistakes) + '\n')
        file.close()
        s = 's'
        if len(Card.cards) == 1:
            s = ''
        my_print(f'{len(Card.cards)} card{s} have been saved.')

    def do_import(self, file_name=None):
        if file_name is None:
            my_print('File name:')
            file_name = my_input()
        cards = []
        try:
            with open(file_name) as file:
                count = 0
                for line in file:
                    term, definition, mistakes = line.strip().split('|')
                    cards.append(Card(term, definition, int(mistakes)))
                    count += 1
                Card.cards = cards
                s = 's'
                if len(Card.cards) == 1:
                    s = ''
                my_print(f'{count} card{s} have been loaded.')
        except FileNotFoundError:
            my_print('File not found.')


if __name__ == '__main__':
    Menu()
