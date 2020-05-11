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
6. Inverse matrix
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
            elif n == 6:
                self._6()
            elif n == 0:
                self._0()
        elif len(self.state) == 2:
            if self.state[1] == 4:
                self._4(n)
            self.state.pop()
        print(self.text)

    @staticmethod
    def _1():
        x, y = map(int, input('Enter size of first matrix: ').split())
        print('Enter first matrix: ')
        matrix_a = Matrix(x, y)
        x, y = map(int, input('Enter size of second matrix: ').split())
        print('Enter second matrix: ')
        matrix_b = Matrix(x, y)
        print(result(adding(matrix_a, matrix_b)))

    @staticmethod
    def _2():
        x, y = map(int, input('Enter size of matrix: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        number = input('Enter constant: ')
        number = float(number) if '.' in number else int(number)
        print(result(multiplication_by_number(matrix_a, number)))

    @staticmethod
    def _3():
        x, y = map(int, input('Enter size of first matrix: ').split())
        print('Enter first matrix: ')
        matrix_a = Matrix(x, y)
        x, y = map(int, input('Enter size of second matrix: ').split())
        print('Enter second matrix: ')
        matrix_b = Matrix(x, y)
        print(result(multiplication(matrix_a, matrix_b)))

    @staticmethod
    def _4(n):
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

    @staticmethod
    def _5():
        x, y = map(int, input('Enter matrix size: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        print(result(determinate(matrix_a)))

    @staticmethod
    def _6():
        x, y = map(int, input('Enter matrix size: ').split())
        print('Enter matrix: ')
        matrix_a = Matrix(x, y)
        print(result(inversion(matrix_a)))

    @staticmethod
    def _0():
        exit()


def result(answer):
    if type(answer) is str and answer.startswith('error'):
        # If error was return:
        # Print Error-message from the code
        return error(int(answer[6:]))
    print('The result is:')
    if type(answer) is list:
        # If answer is Matrix:
        # 1. Convert every digit to str and equalize all columns,
        # 2. every row-list to row-str with spaces,
        # 3. whole list to str with '\n'
        return '\n'.join([' '.join(n) for n in beauty_str_matrix(answer)]) + '\n'
    return str(answer) + '\n'


def error(code):
    if code == 1:
        return 'The operation cannot be performed.\n'
    if code == 2:
        return "This matrix doesn't have an inverse.\n"


def beauty_str_matrix(matrix):
    matrix = rounding(matrix)               # round every digit to float(x.xx) or to int
    for n in range(len(matrix)):
        matrix[n] = [str(m) for m in matrix[n]]             # convert every digit to str
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):                                         # for every column:
            max_len = max([len(matrix[_][m]) for _ in range(len(matrix))])      # find max len of digit
            while len(matrix[n][m]) != max_len:                                 # and add spaces to
                matrix[n][m] = ' ' + matrix[n][m]                               # left side of each one
    return matrix


def rounding(matrix):
    for n in range(len(matrix)):
        matrix[n] = [float('{:.3f}'.format(m)) if float(m) != int(m) else int(m) for m in matrix[n]]
    return matrix


def adding(a, b):
    matrix = []
    if a.n != b.n or a.m != b.m:
        return 'error 1'
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
        return 'error 1'
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
        return 'error 1'
    if a.n == 1:
        return a.matrix[0][0]
    if a.n == 2:
        return a.matrix[0][0] * a.matrix[1][1] - a.matrix[0][1] * a.matrix[1][0]
    if a.n > 2:
        x = 0
        for n in range(a.n):
            x += cofactor(a, a.n - 1, n) * a.matrix[a.n - 1][n]
        return x


def minor(a, x, y):
    matrix = copy.deepcopy(a.matrix)
    for n in range(a.n):
        del matrix[n][y]
    del matrix[x]
    return Matrix(a.n - 1, a.m - 1, matrix)


def inversion(a):
    if determinate(a) == 0:
        return 'error 2'
    return multiplication_by_number(Matrix(a.n, a.m, adj(a)), 1 / determinate(a))


def adj(a):
    matrix = []
    for n in range(a.n):
        matrix.append([])
        for m in range(a.m):
            matrix[n].append(cofactor(a, n, m))
    return transposition_main_diagonal(Matrix(a.n, a.m, matrix))


def cofactor(a, n, m):
    number = (-1) ** ((n + 1) + (m + 1))
    return number * determinate(minor(a, n, m))


menu = Menu()
while True:
    menu.start(int(input('Your choice: ')))

'''
matrix_1 = [[2, -1, 0],
            [0, 1, 2],
            [1, 1, 0]]
matrix_2 = [[2, 1],
            [4, 2]]
matrix_3 = [[0.33, 0, 0.33],
            [-0.33, 0, 0.67],
            [0.17, 0.5, -0.33]]
matrix_a1 = Matrix(3, 3, matrix_1)
matrix_b1 = Matrix(2, 2, matrix_2)
print(result(inversion(matrix_a1)))
print(result(inversion(matrix_b1)))
'''
