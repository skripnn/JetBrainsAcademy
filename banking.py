import random
import sqlite3


class Menu:
    menu = ['Exit',
            'Create an account',
            'Log into account']

    menu_2 = ['Exit',
              'Balance',
              'Add income',
              'Do transfer',
              'Close account',
              'Log out']

    def __init__(self):
        self.card = None
        self.state = [0]
        self.database()
        self.algorithm()

    def database(self):
        conn = sqlite3.connect("card.s3db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE card
                              (id INTEGER PRIMARY KEY NOT NULL,
                               number text,
                               pin text,
                               balance INTEGER DEFAULT 0)
                           """)
        except sqlite3.OperationalError:
            return None

    def algorithm(self):
        while True:
            self.print_menu()
            try:
                n = int(input())
            except ValueError:
                print('Only numbers please')
                continue
            print('')
            if n == 0:
                self._0()
            elif len(self.state) == 1:
                if n == 1:
                    self._1()
                elif n == 2:
                    self.card = self._2()
                    if self.card is not None:
                        self.state.append(2)
            elif len(self.state) == 2:
                if self.state[1] == 2:
                    if n == 1:
                        self._21()
                    elif n == 2:
                        self._22()
                    elif n == 3:
                        self._23()
                    elif n == 4:
                        self._24()
                    elif n == 5:
                        self._25()

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
        print(card.number)
        print('Your card PIN:')
        print(card.pin)

    def _2(self):
        number = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')

        conn = sqlite3.connect("card.s3db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM card WHERE number={number}")
        card = cursor.fetchone()
        if card is not None:
            if pin == card[2]:
                print('\nYou have successfully logged in!')
                return Cards(card)
        print('\nWrong card number or PIN!')
        return None

    def _0(self):
        print('\nBye!')
        exit()

    def _21(self):
        print(f'Balance: {self.card.balance}')

    def _22(self):
        income = int(input('Enter income:\n'))
        self.card.update_balance(income)
        print('Income was added!')

    def _23(self):
        print('Transfer')
        number = input('Enter card number:\n')
        if not self.luhn(number):
            print('Probably you made mistake in the card number. Please try again!')
            return None

        conn = sqlite3.connect("card.s3db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM card WHERE number={number}")
        card = cursor.fetchone()
        if card is None:
            print('Such a card does not exist.')
        else:
            money = int(input('Enter how much money you want to transfer:\n'))
            if money > self.card.balance:
                print('Not enough money!')
            else:
                self.card.transfer(money, Cards(card))
                print('Success!')

    def _24(self):
        conn = sqlite3.connect("card.s3db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM card WHERE number={self.card.number}")
        conn.commit()
        self.card = None
        self.state.pop(-1)
        print('The account has been closed!')

    def _25(self):
        self.card = None
        self.state.pop(-1)
        print('You have successfully logged out!')

    def luhn(self, number):
        numbers = [int(n) for n in number]
        last_symbol = numbers.pop(-1)
        for i, n in enumerate(numbers):
            if i % 2 == 0:
                numbers[i] = n * 2
        for i, n in enumerate(numbers):
            if n > 9:
                numbers[i] = n - 9
        checksum = 10 - sum(numbers) % 10
        if checksum == 10:
            checksum = 0
        if last_symbol != checksum:
            return False
        return True

class Cards:
    mii = 400000

    def __init__(self, card=None):
        if card is None:
            conn = sqlite3.connect("card.s3db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM card")
            ids = cursor.fetchall()
            if len(ids) == 0:
                iin = 1
            else:
                ids = [n[0] for n in ids]
                max_id = max(ids)
                iin = max_id + 1
            pin = ''
            for _ in range(4):
                pin += str(random.randrange(0, 9))

            self.checksum = self.luhn(iin)
            self.number = str(self.mii * 10 ** 10 + iin * 10 + self.checksum)
            self.pin = pin
            self.balance = 0

            conn = sqlite3.connect("card.s3db")
            cursor = conn.cursor()
            sql = f"INSERT INTO card (number, pin) VALUES ('{self.number}', '{self.pin}')"
            cursor.execute(sql)
            conn.commit()
        else:
            self.number = card[1]
            self.pin = card[2]
            self.balance = card[3]

    def luhn(self, iin):
        numbers = [int(n) for n in str(self.mii * 10 ** 10 + iin * 10)]
        for i, n in enumerate(numbers):
            if i % 2 == 0:
                numbers[i] = n * 2
        for i, n in enumerate(numbers):
            if n > 9:
                numbers[i] = n - 9
        checksum = 10 - sum(numbers) % 10
        if checksum == 10:
            checksum = 0
        return checksum

    def update_balance(self, money):
        self.balance += money

        conn = sqlite3.connect("card.s3db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE card SET balance='{self.balance}' WHERE number={self.number}")
        conn.commit()

    def transfer(self, money, card):
        self.update_balance(-money)
        card.update_balance(money)

if __name__ == '__main__':
    Menu()
