import numpy as np


def split(a):
    a_l, a_r = np.hsplit(a, 2)
    return np.vsplit(a_l, 2) + np.vsplit(a_r, 2)


def extend_to_power_of_two(n):
    p = 2
    while p < n:
        p = p * 2
    return p


def product(a, b):
    w = np.shape(a)[0]
    if w == 1:
        return a * b
    else:
        a11, a21, a12, a22 = split(a)
        b11, b21, b12, b22 = split(b)
        p1 = product(a11 + a22, b11 + b22)
        p2 = product(a21 + a22, b11)
        p3 = product(a11, b12 - b22)
        p4 = product(a22, b21 - b11)
        p5 = product(a11 + a12, b22)
        p6 = product(a21 - a11, b11 + b12)
        p7 = product(a12 - a22, b21 + b22)
        c11 = p1 + p4 - p5 + p7
        c12 = p3 + p5
        c21 = p2 + p4
        c22 = p1 - p2 + p3 + p6
        c = np.vstack((np.hstack((c11, c12)),
                       np.hstack((c21, c22))))
        return c


n = int(input())
n_padded = extend_to_power_of_two(n)
a = np.zeros((n_padded, n_padded), int)
b = np.zeros((n_padded, n_padded), int)
for i in range(n):
    a[i, :n] = list(map(int, input().split()))
for i in range(n):
    b[i, :n] = list(map(int, input().split()))
for row in product(a, b)[:n, :n]:
    print(*row)
