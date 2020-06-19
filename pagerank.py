import numpy as np
import numpy.linalg as la
from io import StringIO
import numpy.linalg as la

L = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 0],
    [1 / 3, 1 / 2, 0, 1, 0, 1 / 2],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 2],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1 / 3, 0, 0, 0]
])

# L = np.array([
#     [0, 1 / 2, 1 / 3, 0, 0, 0],
#     [1 / 3, 0, 0, 0, 1 / 2, 1 / 3],
#     [1 / 3, 1 / 2, 0, 1, 0, 0],
#     [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 3],
#     [0, 0, 0, 0, 0, 1 / 3],
#     [0, 0, 1 / 3, 0, 0, 0]
# ])


def get_value_for_print(matrix):
    s = StringIO()
    np.savetxt(s, matrix, fmt="%.3f")
    return s.getvalue()


# e_vals, e_vecs = la.eig(L)
# vec = np.transpose(e_vecs)[0]
#
# for i in vec:
#     x = i * 100 / sum(vec)
#     x = round(x.real, 3)
#     print(x)

r = 100 * np.ones(6) / 6
r = L @ r
print(get_value_for_print(r))

for _ in range(10):
    r = L @ r
print(get_value_for_print(r))

r_prev = r
r_next = L @ r
while la.norm(r_prev - r_next) > 0.001:
    r = r_next
    r_prev = r
    r_next = L @ r
print(get_value_for_print(r))

