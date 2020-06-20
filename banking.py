import random


class Menu:
    menu = ['Exit',
            'Create an account',
            'Log into account']

    menu_2 = ['Exit',
              'Balance',
              'Log out']

    def __init__(self):
        self.card = None
        self.state = [0]
        self.algorithm()

    def algorithm(self):
        while True:
            self.print_menu()
            try:
                n = int(input())
            except ValueError:
                print('Only numbers please')
                continue

            if len(self.state) == 1:
                print('')
                if n == 1:
                    self._1()
                elif n == 2:
                    self.card = self._2()
                    if self.card is not None:
                        self.state.append(2)
                elif n == 0:
                    self._0()
            elif len(self.state) == 2:
                if self.state[1] == 2:
                    if n == 1:
                        print('')
                        self._21()
                    elif n == 2:
                        print('')
                        self._22()
                    elif n == 0:
                        self._0()

    def print_menu(self):
        if len(self.state) == 1:
            menu = self.menu
        elif len(self.state) == 2:
            if self.state[1] == 2:
                menu = self.menu_2

        print('')
        for n, i in enumerate(menu):
            if n == 0:
                last = f'{n}. {i}'
                continue
            print(f'{n}. {i}')
        print(last)


    def _1(self):
        card = Cards()

        print('Your card has been created')
        print('Your card number:')
        print(card.card_number)
        print('Your card PIN:')
        print(card.pin)

    def _2(self):
        card_number = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')
        for card in Cards.cards:
            if card.card_number == card_number:
                if pin == card.pin:
                    print('\nYou have successfully logged in!')
                    return card
                break
        print('\nWrong card number or PIN!')
        return None

    def _0(self):
        print('Bye!')
        exit()

    def _21(self):
        print(f'Balance: {self.card.balance}')

    def _22(self):
        self.card = None
        self.state.pop(-1)
        print('You have successfully logged out!')


class Cards:
    mii = 400000
    cards = []

    def __init__(self):
        if len(Cards.cards) == 0:
            iin = 1
        else:
            iin = Cards.cards[-1].iin + 1
        pin = ''
        for _ in range(4):
            pin += str(random.randrange(0, 9))

        self.iin = iin
        self.checksum = 1
        self.card_number = str(self.mii * 10 ** 10 + self.iin * 10 + self.checksum)
        self.pin = pin
        self.balance = 0
        Cards.cards.append(self)


if __name__ == '__main__':
    Menu()
