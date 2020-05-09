class Matrix:
    matrix = None
    n = None
    m = None

    def __init__(self, n, m):  # Creating a Matrix with N rows and M columns
        self.n = int(n)
        self.m = int(m)
        self.matrix = []
        for _ in range(self.n):
            self.input_row(input())

    def input_row(self, row):
        row = [float(n) if '.' in n else int(n) for n in row.split()]
        self.matrix.append(row)


class Menu:
    text = '''1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
0. Exit'''

    def start(self, n):
        if n == 1:
            self._1()
        elif n == 2:
            self._2()
        elif n == 3:
            self._3()
        elif n == 0:
            self._0()

    def _1(self):
        x, y = map(int, input('Enter size of first matrix: ').split())
        print('Enter first matrix: ')
        matrix_a = Matrix(x, y)
        x, y = map(int, input('Enter size of second matrix: ').split())
        print('Enter second matrix: ')
        matrix_b = Matrix(x, y)
        adding(matrix_a, matrix_b)
        del matrix_a
        del matrix_b

    def _2(self):
        x, y = map(int, input('Enter size of matrix: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        number = input('Enter constant: ')
        number = float(number) if '.' in number else int(number)
        multiplication_by_number(matrix_a, number)
        del matrix_a

    def _3(self):
        x, y = map(int, input('Enter size of first matrix: ').split())
        print('Enter first matrix: ')
        matrix_a = Matrix(x, y)
        x, y = map(int, input('Enter size of second matrix: ').split())
        print('Enter second matrix: ')
        matrix_b = Matrix(x, y)
        multiplication(matrix_a, matrix_b)
        del matrix_a
        del matrix_b

    def _0(self):
        exit()


def error():
    print('The operation cannot be performed.')


def print_result(matrix):
    print('The result is:')
    for n in matrix:
        n = map(str, n)
        print(' '.join(n))


def adding(a, b):
    matrix = []
    if a.n != b.n or a.m != b.m:
        error()
        return None
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            matrix[n].append(a.matrix[n][m] + b.matrix[n][m])
    print_result(matrix)


def multiplication_by_number(a, number):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            matrix[n].append(a.matrix[n][m] * number)
    print_result(matrix)


def multiplication(a, b):
    matrix = []
    if a.m != b.n:
        error()
        return None
    for n in range(a.n):
        matrix.append([])
        for m in range(b.m):
            matrix[n].append([])
            for _ in range(a.m):
                matrix[n][m].append(a.matrix[n][_] * b.matrix[_][m])
            matrix[n][m] = sum(matrix[n][m])
    print_result(matrix)


menu = Menu()
while True:
    print(menu.text)
    menu.start(int(input('Your choice: ')))
    print('')
