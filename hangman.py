import random


class Hangman:
    words = ['python', 'java', 'kotlin', 'javascript']
    word = None
    letters = set()
    hide_word = None
    tried_letters = set()
    tries = None
    status = ''

    def __init__(self):
        print('H A N G M A N')
        self.menu()

    def menu(self):
        self.status = 'menu'
        while self.status == 'menu':
            command = input('Type "play" to play the game, "exit" to quit: ')
            self.check_menu_choose(command)

    def check_menu_choose(self, command):
        if command == 'exit':
            exit()
        elif command == 'play':
            self.start()

    def start(self):
        self.status = 'game'
        self.tried_letters.clear()
        self.word = random.choice(self.words)
        self.letters = set(self.word)
        self.hide_word = '-' * len(self.word)
        self.tries = 8
        while self.tries > 0 and self.hide_word != self.word:
            self.trying()
        self.game_over()

    def trying(self):
        print('')
        print(self.hide_word)
        letter = input('Input a letter: ')
        if self.check_errors(letter):
            return None
        self.tried_letters.add(letter)
        if self.check_letter(letter):
            self.set_hide_word()
        else:
            self.tries -= 1

    def set_hide_word(self):
        self.hide_word = ''
        for i in self.word:
            if i in self.tried_letters:
                self.hide_word += i
            else:
                self.hide_word += '-'

    def check_errors(self, letter):
        if letter in self.tried_letters:
            print('You already typed this letter')
            return True
        if len(letter) != 1:
            print('You should print a single letter')
            return True
        if not letter.islower():
            print('It is not an ASCII lowercase letter')
            return True
        return False

    def check_letter(self, letter):
        if letter in self.letters:
            return True
        print('No such letter in the word')
        return False

    def game_over(self):
        if self.letters <= self.tried_letters:
            print(self.hide_word)
            print('You guessed the word!')
            print('You survived!')
        else:
            print('You are hanged!')
        print('')
        self.menu()


game = Hangman()
