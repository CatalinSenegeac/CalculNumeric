import numpy as np


def readAandF(input_folder, index):
    # reading A matrix data
    with open(input_folder + '/a' + str(index) + '.txt', 'r') as f:
        n = int(f.readline())
        p = int(f.readline())
        precision = 10 ** (-p)
        q = int(f.readline())
        # empty line
        f.readline()
        a = getLineInfo(f)
        b = getLineInfo(f)
        c = getLineInfo(f)
        if len(a) != n or len(b) != n - q or len(c) != len(c):
            raise ValueError("Invalid A file format!")

        if not verify_array_not_null(a, precision):
            raise ValueError("Invalid main diagonal in A file!")

    with open(input_folder + '/f' + str(index) + '.txt', 'r') as f:
        f_len = int(f.readline())
        if f_len != n:
            raise ValueError('Invalid f file')
        # empty line
        f.readline()
        f = getLineInfo(f)
        if len(f) != f_len:
            raise ValueError("Invalid F file format!")

    return n, p, q, precision, a, b, c, f


def getLineInfo(file_desc):
    lines = []
    line = file_desc.readline()
    while line and not line == "\n":
        lines.append(float(line))
        line = file_desc.readline()

    return lines


def verify_array_not_null(number_array, precision):
    if np.any(abs(np.array(number_array)) <= precision):
        return False
    return True


# also includes bonus
def compute_xc_using_xp(xp, n, p, q, a, b, c, f):
    xc = np.copy(xp)
    for i in range(n):
        # since the matrix is rare, we will select elements only from the three diagonals
        b_sum = 0
        c_sum = 0
        if i >= q:
            b_sum = b[i-1] * xp[i - q]
        if i < n - p:
            c_sum = c[i-1] * xp[i + p]
        xc[i] = (f[i] - b_sum - c_sum) / a[i]

    return xc


def approximate_using_gs(n, p, q, precision, a, b, c, f, k_max=10000):
    x_prev = np.zeros(n)
    x_current = compute_xc_using_xp(x_prev, n, p, q, a, b, c, f)
    delta_x = np.linalg.norm(x_current - x_prev)
    k = 1
    while precision <= delta_x <= 10 ** 8 and k < k_max:
        x_prev = x_current
        x_current = x_current = compute_xc_using_xp(x_prev, n, p, q, a, b, c, f)
        delta_x = np.linalg.norm(x_current - x_prev)
        k += 1
    if delta_x < precision:
        return x_current
    else:
        raise ValueError("Divergenta")


if __name__ == '__main__':
    for i in range(1,6):
        n, p, q, precision, a, b, c, f = readAandF('./inputs', i)
        try:
            x_gs = approximate_using_gs(n, p, q, precision, a, b, c, f)
        except:
            print("Divergenta")
        else:
            print(x_gs)
