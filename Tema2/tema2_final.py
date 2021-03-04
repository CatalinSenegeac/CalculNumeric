import numpy as np
from math import sqrt
from copy import deepcopy
from scipy.linalg import lu_factor, lu_solve


# citeste matricea in modul specificat de user si returneaza precizia si matricea
def get_matrix_from_user():
    epsilon = float(input("Introduceti precizia calculelor:\n"))

    read_mode = input("Cum vreti sa introduceti matricea? (fisier/random/consola)\n")

    if read_mode == 'fisier':
        file = input("Introduceti numele fisierului:\n")
        matrix = read_array_from_file(file)

    elif read_mode == 'random':
        n = int(input("Introduceti dimensiunea sistemului:\n"))
        matrix = generate_symmetric_matrix(n)

    elif read_mode == 'consola':
        n = int(input("Introduceti dimensiunea sistemului:\n"))
        matrix = read_matrix_from_console(n)

    return epsilon, matrix


# pentru citire array de la user
def get_array_from_user(n):
    read_mode = input("Cum vreti sa introduceti vectorul? (fisier/random/consola)\n")

    if read_mode == 'fisier':
        file = input("Introduceti numele fisierului:\n")
        array = read_array_from_file(file)

    elif read_mode == 'random':
        array = np.random.uniform(-10, 10, size=n)

    elif read_mode == 'consola':
        array = []
        for i in range(n):
            array.append(float(input("Introduceti elementul %d" % i)))

    return np.array(array)


# functii de citire/scriere
def read_matrix_from_console(size):
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(input("Introduceti elementul (%d, %d): \n" % (i, j)))
        matrix.append(row)

    return np.array(matrix)


def read_array_from_file(file):
    return np.loadtxt(file, dtype='float64', delimiter=' ')


def write_array_to_file(matrix, file):
    np.savetxt(file, matrix, delimiter=' ')


# generare matrice simetrica cu elemente random
def generate_symmetric_matrix(size):
    initial_matrix = np.random.uniform(-10, 10, size=(size, size))
    symmetric = np.array((initial_matrix + initial_matrix.T) / 2)
    return symmetric


# functii de validare (daca e simetrica, daca e pozitiv definita)
def check_symmetric(a, precision=1e-8):
    return np.all(np.abs(a - a.T) < precision)


# A matrix is positive definite if it's symmetric and all its eigenvalues are positive
# https://www.math.utah.edu/~zwick/Classes/Fall2012_2270/Lectures/Lecture33_with_Examples.pdf
def is_pos_def(matrix):
    if not check_symmetric(matrix):
        raise ValueError("Matricea trebuie sa fie simetrica!")
    return np.all(np.linalg.eigvals(matrix) > 0)


def get_cholesky_decomposition(matrix, epsilon):
    n = len(matrix)
    d = [matrix[i][i] for i in range(n)]
    try:
        for p in range(n):
            # l_pp
            matrix[p][p] = sqrt(d[p] - sum([matrix[p][j] ** 2 for j in range(p)]))

            # restul coloanei
            for i in range(p + 1, n):
                matrix[i][p] = division(
                    matrix[i][p] - sum([matrix[i][j] * matrix[p][j] for j in range(p)]),
                    matrix[p][p],
                    epsilon)
        return d
    except:
        print("Matricea nu e definita pozitiv.")


# divizie cu verificarea preciziei.
def division(a, b, epsilon):
    if abs(b) > epsilon:
        return a / b

    raise ValueError("Numitor nul!")


def compute_determinant_using_L(cholesky_l):
    det = 1
    for i in range(len(cholesky_l)):
        det *= cholesky_l[i][i]

    return det ** 2


# metoda substitutiei directe
def direct_substitution_method(cholesky_l, b, epsilon):
    solution = []

    for i in range(len(cholesky_l)):
        solution.append(division(
            b[i] - sum([cholesky_l[i][j] * solution[j] for j in range(i)]),
            cholesky_l[i][i],
            epsilon)
        )

    return solution


def inverse_substitution_method(cholesky_l, b, epsilon):
    solution = np.zeros(len(cholesky_l))
    for i in reversed(range(len(cholesky_l))):
        solution[i] = division(
            b[i] - sum([cholesky_l[j][i] * solution[j] for j in range(i + 1, len(cholesky_l))]),
            cholesky_l[i][i],
            epsilon
        )
    return solution


def as_column_vector(arr):
    return arr.reshape(-1, 1)


def multiply(cholesky_l, x, diag):
    result = np.zeros((len(cholesky_l), len(x[0])))

    for i in range(len(cholesky_l)):
        for j in range(len(x[0])):
            for k in range(len(x)):
                if i > k:
                    result[i][j] += cholesky_l[k][i] * x[k][j]
                elif i == k:
                    result[i][j] += diag[i] * x[k][j]
                else:
                    result[i][j] += cholesky_l[i][k] * x[k][j]

    return result


def euclidean_norm(matrix):
    return sqrt(sum([matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[0]))]))


def lu_experiment(matrix, b):
    lu, piv = lu_factor(matrix)
    print("LU MATRIX:\n", lu)
    print("PIVOT MATRIX:\n", piv)

    x = lu_solve((lu, piv), b)
    print("LU SOLUTION:\n", x)


def cholesky_inverse(cholesky_l, epsilon):
    columns = []
    for j in range(len(cholesky_l)):
        e = [1 if i == j else 0 for i in range(len(cholesky_l))]
        y = direct_substitution_method(cholesky_l, e, epsilon)
        x = inverse_substitution_method(cholesky_l, y, epsilon)
        columns.append(x)

    return np.column_stack(tuple(columns))


# bonus

def map_sym_matrix_to_array(matrix):
    return [matrix[i][j] for i in range(len(matrix)) for j in range(i + 1)]


def get_matrix_size(length):
    n = 1
    while n * (n + 1) / 2 != length:
        n += 1

    return n


def get_arr_index(i, j):
    i0 = i
    j0 = j
    if i0 < j0:
        aux = i0
        i0 = j0
        j0 = aux

    return int(i0 * (i0 + 1) / 2) + j0


def get_cholesky_decomposition_arr(arr, n, epsilon):
    l = np.zeros(int(n * (n + 1) / 2))

    for p in range(n):
        l[get_arr_index(p, p)] = sqrt(arr[get_arr_index(p, p)] - sum([l[get_arr_index(p, j)] ** 2 for j in range(p)]))

        for i in range(p + 1, n):
            l[get_arr_index(i, p)] = division(
                arr[get_arr_index(i, p)] - sum([l[get_arr_index(i, j)] * l[get_arr_index(p, j)] for j in range(p)]),
                l[get_arr_index(p, p)],
                epsilon
            )

    return l


def direct_substitution_method_arr(arr, b, n, epsilon):
    solution = []

    for i in range(n):
        solution.append(division(
            b[i] - sum([arr[get_arr_index(i, j)] * solution[j] for j in range(i)]),
            arr[get_arr_index(i, i)],
            epsilon)
        )
    return solution


def inverse_substitution_method_arr(arr, b, n, epsilon):
    solution = np.zeros(n)

    for i in reversed((range(n))):
        solution[i] = division(
            b[i] - sum([l[get_arr_index(j, i)] * solution[j] for j in range(i + 1, n)]),
            l[get_arr_index(i, i)],
            epsilon
        )
    return solution


if __name__ == '__main__':
    e, m = get_matrix_from_user()
    m_initial = deepcopy(m)
    print("Matricea initiala:\n", m_initial)
    diag = get_cholesky_decomposition(m, e)
    print("Dupa descompunerea cholesky:\n", m, diag)
    print("Determinantul calculat cu L: ", compute_determinant_using_L(m))
    print("Determinantul adevarat: ", np.linalg.det(m_initial))
    b = get_array_from_user(len(m))
    y = direct_substitution_method(m, b, e)
    print("Y is:\n", y)
    x_chol = inverse_substitution_method(m, y, e)
    print("X_chol is:\n", x_chol)
    norm = euclidean_norm(multiply(m, as_column_vector(x_chol), diag) - as_column_vector(b))
    print("|A_init * x_chol - b|_2 = ", norm)
    lu_experiment(m_initial, b)

    inverse = cholesky_inverse(m, e)
    print("THE CHOLESKY INVERSE IS:\n", inverse)
    print("NORM OF A^-1 difference:\n", np.linalg.norm(inverse - np.linalg.inv(m_initial)))

    print("BONUS PART")
    m_arr = map_sym_matrix_to_array(m_initial)
    print("A_init mapped as array: ", map_sym_matrix_to_array(m_initial))
    n = len(m_initial)
    l = get_cholesky_decomposition_arr(m_arr, n, e)
    print("L array is: ", l)
    y = direct_substitution_method_arr(l, b, n, e)
    print("Y is:\n", y)
    x_chol = inverse_substitution_method_arr(l, y, n, e)
    print("X_chol is:\n", x_chol)

