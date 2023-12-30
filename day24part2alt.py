import numpy as np
import sympy as sp

p1 = np.array([[19], [13], [30]])
v1 = np.array([[-2], [1], [-2]])

p2 = np.array([[18], [19], [22]])
v2 = np.array([[-1], [-1], [-2]])

p3 = np.array([[20], [25], [34]])
v3 = np.array([[-2], [-2], [-4]])

p4 = np.array([[12], [31], [28]])
v4 = np.array([[-1], [-2], [-1]])


# t1, w1, w2 (=t2 * w1), t3
A = np.concatenate([v1, p2 - p1, v2, -v3, p3 - p1], axis=1)
Ar = np.array(sp.Matrix(A).rref()[0])
# print(Ar)

t1 = Ar[0, 3]
w1 = Ar[1, 3]

C1 = (1 - w1) * p1 + w1 * p2 + t1 * v1

def do_lines_intersect(p1, v1, p2, v2):
    A = np.concatenate([v1, -v2, p2 - p1], axis=1)
    Ar = np.array(sp.Matrix(A).rref()[0])
    print(Ar)

do_lines_intersect(p2, v2, C1, v2)


# C = p1 + t1 * v1 + w1 * p2

# # w2, w1, t4
# B = np.concatenate([v2, -p1, -v4, p4 - C], axis=1)
# Br = np.array(sp.Matrix(B).rref()[0])
# # print(Br)

# w2 = Br[0, 3]
# w1 = Br[1, 3]
# t4 = Br[2, 3]
# t2 = w2 / w1
# t3 = (w2 - Ar[2, 3] // 2)


# i1 = p1 + t1 * v1
# i2 = p2 + t2 * v2
# i3 = p3 + t3 * v3
# i4 = p4 + t4 * v4

# c1 = i2 - i1
# c2 = i3 - i2
# c3 = i4 - i3

# def are_multiples(vector1, vector2):
#     f = vector2 / vector1
#     return f[0, 0] == f[1, 0] == f[2, 0]

# print(are_multiples(c1, c2))
# print(are_multiples(c2, c3))