class Matrix:
    matrix = None
    n = None
    m = None

    def __init__(self, n, m):           # Creating a Matrix with N rows and M columns
        self.n = int(n)
        self.m = int(m)
        self.matrix = []
        for _ in range(self.n):
            self.input_row(input())

    def input_row(self, row):
        row = [int(n) for n in row.split()]
        self.matrix.append(row)


def print_result(matrix):
    for n in matrix:
        n = map(str, n)
        print(' '.join(n))


def adding(a, b):
    matrix = []
    if a.n != b.n or a.m != b.m:
        print('ERROR')
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


x, y = map(int, input().split())
matrix_a = Matrix(x, y)
number = int(input())
multiplication_by_number(matrix_a, number)
