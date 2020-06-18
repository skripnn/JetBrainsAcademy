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

s = StringIO()
np.savetxt(s, L, fmt="%.3f")
print(s.getvalue(), end='')

e_vals, e_vecs = la.eig(L)
vec = np.transpose(e_vecs)[0]

for i in vec:
    x = i * 100 / sum(vec)
    x = round(x.real, 3)
    print(x)
