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


def adding(a, b):
    result = []
    if a.n != b.n or a.m != b.m:
        print('ERROR')
        return None
    for n in range(a.n):
        result.append([])
        for m in range(a.m):
            result[n].append(a.matrix[n][m] + b.matrix[n][m])
    for n in result:
        n = map(str, n)
        print(' '.join(n))


x, y = map(int, input().split())
matrix_a = Matrix(x, y)
x, y = map(int, input().split())
matrix_b = Matrix(x, y)
adding(matrix_a, matrix_b)
