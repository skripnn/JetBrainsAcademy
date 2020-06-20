import random
import sqlite3


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


if __name__ == '__main__':
    Menu()
