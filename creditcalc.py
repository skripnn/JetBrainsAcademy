import math
import sys


class CreditCalculator:
    state = []
    p = None
    a = None
    i = None
    n = None
    type = None

    def __init__(self, *args):
        kwargs = {}
        for arg in args:
            if args.index(arg) == 0:
                continue
            if arg.startswith('--'):
                temp = arg.split('=')
                kwargs[temp[0]] = temp[1]
            else:
                self.error()

        for key, value in kwargs.items():
            if key == '--type':
                if value == 'annuity' or value == 'diff':
                    self.type = value
                else:
                    self.error()
            elif key == '--payment':
                if kwargs['--type'] == 'diff':
                    self.error()
                self.a = float(value)
            elif key == '--principal':
                self.p = int(value)
            elif key == '--periods':
                self.n = int(value)
            elif key == '--interest':
                self.i = self.find_i(float(value))
            else:
                self.error()

        if self.p is None:
            self.state.append('p')
        if self.a is None:
            self.state.append('a')
        if self.n is None:
            self.state.append('n')
        if self.i is None:
            self.state.append('i')
        if len(self.state) != 1:
            self.error()

        if self.type == 'diff':
            self.find_d()
        elif self.type == 'annuity':
            self.result()

    def error(self):
        print('Incorrect parameters')
        exit()

    def s(self, var):
        if var == 1:
            return ''
        return 's'

    def result(self):
        a = self.a
        p = self.p
        i = self.i
        n = self.n

        if self.state[0] == 'n':
            self.n = math.ceil(math.log(a / (a - i * p), 1 + i))
            years = self.n // 12
            if years == 0:
                years = ''
            else:
                years = f'{years} year{self.s(years)}'
            months = self.n % 12
            if months == 0:
                months = ''
            else:
                months = f'{months} month{self.s(months)}'
            link = ''
            if years != '' and months != '':
                link = ' and '
            print(f'You need {years}{link}{months} to repay this credit!')

        elif self.state[0] == 'a':
            self.a = math.ceil(p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
            print(f'Your annuity payment = {self.a}!')

        elif self.state[0] == 'p':
            self.p = math.floor(a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
            print(f'Your credit principal = {self.p}!')

        overpayment = int(self.a * self.n - self.p)
        print(f'Overpayment = {overpayment}')
        exit()

    def find_i(self, c_i):
        return c_i / 12 / 100

    def find_d(self):
        p = self.p
        i = self.i
        n = self.n
        overpayment = 0

        for m in range(n):
            m += 1
            d = math.ceil(p / n + i * (p - (p * (m - 1)) / n))
            print(f'Month {m}: paid out {d}')
            overpayment += d
        overpayment -= p
        print(f'\nOverpayment = {overpayment}')
        exit()


project = CreditCalculator(*sys.argv)
