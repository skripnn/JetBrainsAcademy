import copy


class Matrix:

    def __init__(self, n, m, matrix=None):  # Creating a Matrix with N rows and M columns
        self.n = int(n)
        self.m = int(m)
        if matrix is None:
            self.matrix = []
            for _ in range(self.n):
                self.input_row(input())
        else:
            self.matrix = matrix

    def input_row(self, row):  # Input one row
        row = [float(n) if '.' in n else int(n) for n in row.split()]
        self.matrix.append(row)


class Menu:
    text = '''1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
0. Exit'''

    text_4 = '''
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line'''

    def __init__(self):
        print(self.text)
        self.state = [0]

    def start(self, n):  # Menu algorithm
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
                return None
            elif n == 5:
                self._5()
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
        print(result(adding(matrix_a, matrix_b)))
        del matrix_a
        del matrix_b

    def _2(self):
        x, y = map(int, input('Enter size of matrix: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        number = input('Enter constant: ')
        number = float(number) if '.' in number else int(number)
        print(result(multiplication_by_number(matrix_a, number)))
        del matrix_a

    def _3(self):
        x, y = map(int, input('Enter size of first matrix: ').split())
        print('Enter first matrix: ')
        matrix_a = Matrix(x, y)
        x, y = map(int, input('Enter size of second matrix: ').split())
        print('Enter second matrix: ')
        matrix_b = Matrix(x, y)
        print(result(multiplication(matrix_a, matrix_b)))
        del matrix_a
        del matrix_b

    def _4(self, n):
        x, y = map(int, input('Enter matrix size: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        if n == 1:
            print(result(transposition_main_diagonal(matrix_a)))
        elif n == 2:
            print(result(transposition_side_diagonal(matrix_a)))
        elif n == 3:
            print(result(transposition_by_vertical(matrix_a)))
        elif n == 4:
            print(result(transposition_by_horizontal(matrix_a)))
        del matrix_a

    def _5(self):
        x, y = map(int, input('Enter matrix size: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        print(result(determinate(matrix_a)))
        del matrix_a

    def _0(self):
        exit()


def result(answer):
    if answer == 'error':
        return 'The operation cannot be performed.\n'
    print('The result is:')
    if type(answer) is list:
        # If answer is Matrix: every int to str, every row-list to row-str with spaces, whole list to str with '\n'
        return '\n'.join([' '.join(map(str, n)) for n in answer]) + '\n'
    return str(answer) + '\n'


def adding(a, b):
    matrix = []
    if a.n != b.n or a.m != b.m:
        return 'error'
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            matrix[n].append(a.matrix[n][m] + b.matrix[n][m])
    return matrix


def multiplication_by_number(a, number):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            matrix[n].append(a.matrix[n][m] * number)
    return matrix


def multiplication(a, b):
    matrix = []
    if a.m != b.n:
        return 'error'
    for n in range(a.n):
        matrix.append([])
        for m in range(b.m):
            matrix[n].append([])
            for _ in range(a.m):
                matrix[n][m].append(a.matrix[n][_] * b.matrix[_][m])
            matrix[n][m] = sum(matrix[n][m])
    return matrix


def transposition_main_diagonal(a):
    matrix = []
    for n in range(a.m):
        matrix.append([])
        for m in range(a.n):
            x = m
            y = n
            matrix[n].append(a.matrix[x][y])
    return matrix


def transposition_side_diagonal(a):
    matrix = []
    for n in range(a.m):
        matrix.append([])
        for m in range(a.n):
            x = (a.n - 1) - m
            y = (a.m - 1) - n
            matrix[n].append(a.matrix[x][y])
    return matrix


def transposition_by_vertical(a):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            x = n
            y = (a.m - 1) - m
            matrix[n].append(a.matrix[x][y])
    return matrix


def transposition_by_horizontal(a):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            x = (a.n - 1) - n
            y = m
            matrix[n].append(a.matrix[x][y])
    return matrix


def determinate(a):
    if a.n != a.m:
        return 'error'
    if a.n == 1:
        return a.matrix[0][0]
    if a.n == 2:
        return a.matrix[0][0] * a.matrix[1][1] - a.matrix[0][1] * a.matrix[1][0]
    if a.n > 2:
        x = 0
        for n in range(a.n):
            x += (-1) ** (a.n + (n + 1)) * a.matrix[a.n - 1][n] * determinate(minor(a, n))
        return x


def minor(a, i):
    matrix = copy.deepcopy(a.matrix)
    for n in range(a.n):
        del matrix[n][i]
    matrix.pop()
    return Matrix(a.n - 1, a.m - 1, matrix)


menu = Menu()
while True:
    menu.start(int(input('Your choice: ')))

