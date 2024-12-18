import numpy as np
from math import sqrt, pi, exp, log

SIZE = 256
N_MAXp2 = SIZE + 2
N_MAX2 = SIZE * SIZE
arr_a = np.zeros((N_MAXp2, N_MAXp2), dtype=float)
arr_b = np.zeros((N_MAXp2, N_MAXp2), dtype=int)


def get(i, N):
    result = 0
    if i > N:
        result = 1
    elif i < 1:
        result = N
    else:
        result = i
    return result


def fill(i, j, c, N, p):
    di = [1, -1, 0, 0]
    dj = [0, 0, 1, -1]
    st = [(0, 0) for _ in range(N**2)]
    sq = 0
    s_top = 1
    st[s_top - 1] = (i, j)
    while s_top != 0:
        i, j = st[s_top - 1]
        s_top -= 1
        arr_b[i][j] = c
        sq += 1
        for k in range(4):
            ti = get(i + di[k], N)
            tj = get(j + dj[k], N)
            if arr_a[ti][tj] > p and arr_b[ti][tj] == 0:
                arr_b[ti][tj] = -1
                s_top += 1
                st[s_top - 1] = (ti, tj)
    return sq


def init_arrays(N, array):
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            arr_a[i][j] = array[(j - 1) + N * (i - 1)]
            arr_b[i][j] = 0


def calcPrecipitate2d(array, p, N, ell):
    init_arrays(N, array)
    c_cnt = 0
    nOfIslands = 0
    meanRadius = 0.0

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if arr_a[i][j] >= p and arr_b[i][j] == 0:
                c_cnt += 1
                tmp = fill(i, j, c_cnt, N, p)
                meanRadius += (1.0 * tmp / pi) ** 0.5
                nOfIslands += 1
                if tmp < 4:
                    c_cnt -= 1
                    arr_b[i][j] = -1
    if nOfIslands != 0:
        meanRadius /= nOfIslands
        Rp = meanRadius * ell * 1e9
        Np = exp(1.5 * log(nOfIslands)) / exp(3.0 * log(N * ell)) * 1e-27
    else:
        Rp = 0.0
        Np = 0.0
    return Rp, Np
