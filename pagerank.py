import numpy as np
import numpy.linalg as la
from io import StringIO

L = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 0],
    [1 / 3, 1 / 2, 0, 1, 0, 1 / 2],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 2],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1 / 3, 0, 0, 0]
])

L_task = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 1 / 3],
    [1 / 3, 1 / 2, 0, 1, 0, 0],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 3],
    [0, 0, 0, 0, 0, 1 / 3],
    [0, 0, 1 / 3, 0, 0, 0]
])

L2 = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 0, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 0, 0],
    [1 / 3, 1 / 2, 0, 1, 0, 1 / 3, 0],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 3, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1 / 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1 / 3, 1]
])


L2_task = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 100, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 100, 0],
    [1 / 3, 1 / 2, 0, 1, 0, 100, 0],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 100, 0],
    [0, 0, 0, 0, 0, 100, 0],
    [0, 0, 1 / 3, 0, 0, 100, 0],
    [0, 0, 0, 0, 0, 100, 1]
])


def print_value(matrix):
    s = StringIO()
    np.savetxt(s, matrix, fmt="%.3f")
    print(s.getvalue())


def page_rank_vector(matrix, r=None):
    if r is None:
        x = len(matrix)
        r = 100 * np.ones(x) / x
    return matrix @ r


def page_rank_vector_precision(matrix, r=None, precision=0.01):
    r_prev = matrix
    r_next = page_rank_vector(matrix, r)
    check = float(str(la.norm(r_prev - r_next))[:5])
    while check > precision:
        r_prev = r_next
        r_next = page_rank_vector(matrix, r_prev)
        check = float(str(la.norm(r_prev - r_next))[:5])
    return r_next


def stage_1(matrix):
    print_value(matrix)
    e_vals, e_vecs = la.eig(matrix)
    vec = np.transpose(e_vecs)[0]

    for i in vec:
        x = i * 100 / sum(vec)
        x = round(x.real, 3)
        print(x)


def stage_2(matrix):
    r = page_rank_vector(matrix)
    print_value(r)

    for _ in range(10):
        r = page_rank_vector(matrix, r)
    print_value(r)

    r = page_rank_vector_precision(matrix, r, 0.001)
    print_value(r)


def stage_3(matrix):
    x = len(matrix)
    print_value(matrix)

    d = 0.5
    j = np.ones((x, x))
    m = d * matrix + ((1 - d) / x) * j

    r = page_rank_vector_precision(matrix)
    print_value(r)

    r = page_rank_vector_precision(m)
    print_value(r)


stage_3(L2)
