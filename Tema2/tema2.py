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


# Factorizare Cholesky
def get_cholesky_decomposition(matrix, epsilon):
    n = len(matrix)
    d = [matrix[i][i] for i in range(n)]
    try:
        for p in range(n):
            # elementele de deasupra diagonalei principale vor fi 0
            for i in range(p):
                matrix[i][p] = 0
            # l_pp
            matrix[p][p] = sqrt(d[p] - sum([matrix[p][j] ** 2 for j in range(p)]))

            # restul coloanei
            for i in range(p + 1, n):
                matrix[i][p] = division(
                    matrix[i][p] - sum([matrix[i][j] * matrix[p][j] for j in range(p)]),
                    matrix[p][p],
                    epsilon)
    except:
        print("Matricea nu e definita pozitiv.")


# divizie cu verificarea preciziei.
def division(a, b, epsilon):
    if abs(b) > epsilon:
        return a / b

    raise ValueError("Numitor nul!")


def compute_determinant_using_L(cholesky_l):
    return np.linalg.det(cholesky_l) * np.linalg.det(cholesky_l.T)


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


def inverse_substitution_method(transposed_cholesky_l, b, epsilon):
    solution = np.zeros(len(transposed_cholesky_l))

    for i in reversed(range(len(transposed_cholesky_l))):
        solution[i] = division(
            b[i] - sum([transposed_cholesky_l[i][j] * solution[j] for j in range(i + 1, len(transposed_cholesky_l))]),
            transposed_cholesky_l[i][i],
            epsilon
        )

    return solution


def as_column_vector(arr):
    return arr.reshape(-1, 1)


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
        x = inverse_substitution_method(cholesky_l.T, y, epsilon)
        columns.append(x)

    return np.column_stack(tuple(columns))


if __name__ == '__main__':
    e, m = get_matrix_from_user()
    m_initial = deepcopy(m)
    print("Matricea initiala:\n", m_initial)
    get_cholesky_decomposition(m, e)
    print("L:\n", m)
    print("Determinantul calculat cu L: ", compute_determinant_using_L(m))
    print("Determinantul adevarat: ", np.linalg.det(m_initial))
    print("Urmeaza sa introduceti b, pentru a evidentia cum putem "
          "folosi descompunerea choleski pentru a rezolva sisteme liniare de tip Ax = b")
    b = get_array_from_user(len(m))

    y = direct_substitution_method(m, b, e)
    x = inverse_substitution_method(m.T, y, e)
    print("THE CHOLESKY X IS:\n", x)
    print("NORM IS: ", np.linalg.norm(np.dot(m_initial, x) - b))
    lu_experiment(m_initial, b)
    inverse = cholesky_inverse(m, e)
    print("THE CHOLESKY INVERSE IS:\n", inverse)
    print("NORM OF A^-1 difference:\n", np.linalg.norm(inverse - np.linalg.inv(m_initial)))
