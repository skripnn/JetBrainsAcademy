class Matrix:

    def __init__(self, n, m):  # Creating a Matrix with N rows and M columns
        self.n = int(n)
        self.m = int(m)
        self.matrix = []
        for _ in range(self.n):
            self.input_row(input())

    def input_row(self, row):   # Input one row
        row = [float(n) if '.' in n else int(n) for n in row.split()]
        self.matrix.append(row)


class Menu:
    text = '''1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
0. Exit'''

    text_4 = '''
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line'''

    def __init__(self):
        print(self.text)
        self.state = [0]

    def start(self, n):         # Menu algorithm
        if len(self.state) == 1:
            if n == 1:
                self._1()
            elif n == 2:
                self._2()
            elif n == 3:
                self._3()
            elif n == 4:
                print(self.text_4)
                self.state.append(4)
            elif n == 0:
                self._0()
        elif len(self.state) == 2:
            if self.state[1] == 4:
                self._4(n)
            self.state.pop()
            print(self.text)

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

    def _4(self, n):
        x, y = map(int, input('Enter matrix size: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        if n == 1:
            transposition_main_diagonal(matrix_a)
        elif n == 2:
            transposition_side_diagonal(matrix_a)
        elif n == 3:
            transposition_by_vertical(matrix_a)
        elif n == 4:
            transposition_by_horizontal(matrix_a)

    def _0(self):
        exit()


def error():
    print('The operation cannot be performed.')


def print_result(matrix):
    print('The result is:')
    for n in matrix:
        n = map(str, n)
        print(' '.join(n))
    print('')


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


def transposition_main_diagonal(a):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            x = m
            y = n
            matrix[n].append(a.matrix[x][y])
    print_result(matrix)


def transposition_side_diagonal(a):
    matrix = []
    for n in range(a.m):
        matrix.append([])
        for m in range(a.n):
            x = (a.n - 1) - m
            y = (a.m - 1) - n
            matrix[n].append(a.matrix[x][y])
    print_result(matrix)


def transposition_by_vertical(a):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            x = n
            y = (a.m - 1) - m
            matrix[n].append(a.matrix[x][y])
    print_result(matrix)


def transposition_by_horizontal(a):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            x = (a.n - 1) - n
            y = m
            matrix[n].append(a.matrix[x][y])
    print_result(matrix)


menu = Menu()
while True:
    menu.start(int(input('Your choice: ')))
