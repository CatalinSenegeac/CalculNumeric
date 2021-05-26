import math as m
import numpy as np
from numpy import matrix
from scipy.linalg import lu, svd  #pus pentru calcularea descompunerii Cholesky
from scipy.linalg import svd #libraria pentru calculul svd

# cazul: p = n ----------------------------------------------------------------------------------------------------------------------------------------------------
def Jacobi(A, epsilon):
    n = len(A)
    k = 0
    k_max = 100000
    U = np.identity(n)
    p, q = calculate_p_and_q(A)
    alfa = calculate_alfa(A, p, q)
    s, c, t = calculate_SCT(alfa)
    while abs(A[p][q]) > epsilon and k <= k_max:
        A = calculate_matrixA_rotation(A, p, q, c, s, t)
        U = recalculate_U(U, p, q, c, s)
        p, q = calculate_p_and_q(A)
        alfa = calculate_alfa(A, p, q)
        s, c, t = calculate_SCT(alfa)
        k += 1
    print("Lambda: ")
    print(np.round(A, 6))
    return (A.diagonal(), U)


def calculate_p_and_q(A):
    maximum_value = 0
    p = -1
    q = -1
    for i in range(0, len(A)):
        for j in range(0, i):
            if abs(A[i][j]) > maximum_value:
                maximum_value = abs(A[i][j])
                p = i
                q = j

    return (p, q)


def calculate_alfa(A, p, q):
    return ((A[p][p] - A[q][q]) / (2 * A[p][q]))


def calculate_SCT(alfa):
    if alfa >= 0:
        t = -alfa + m.sqrt(alfa * alfa + 1)
    else:
        t = -alfa - m.sqrt(alfa * alfa + 1)
    c = 1 / m.sqrt((1 + t * t))
    s = t / m.sqrt((1 + t * t))

    return (s, c, t)

def calculate_matrixA_rotation(A, p, q, c, s, t):
    for j in range(0, len(A)):
        if j != p and j != q:
            A[p][j] = (c * A[p][j]) + (s * A[q][j])
            A[j][q] = (-s * A[j][p]) + (c * A[q][j])
            A[q][j] = A[j][q]
            A[j][p] = A[p][j]
    A[p][p] = A[p][p] + (t * A[p][q])
    A[q][q] = A[q][q] - (t * A[p][q])
    A[p][q] = 0
    A[q][p] = 0
    return A


def recalculate_U(U, p, q, c, s):
    for i in range(0, len(U)):
        Uip_vechi = U[i][p]
        U[i][p] = c * U[i][p] + s * U[i][q]
        U[i][q] = -s * Uip_vechi + c * U[i][q]
    return U

def calculate_norma(A, lambda_diagonal, U):
    norma = abs(A * U - U * lambda_diagonal)
    return norma

def calculate_S_I(S, p, n):
    S_I = [[0 for i in range(p)] for j in range(n)]
    for i in range(p):
        for j in range(n):
            if i == j:
                S_I[i][j] = 1 / S[i]
    return S_I
def show_information_for_p1(A, epsilon):
    U, lambda_diagonal = Jacobi(A, epsilon)
    norma = calculate_norma(A, lambda_diagonal, U)
    print("Norma matriciala este: ")
    print(np.linalg.norm(norma))


def point1(A1, A2, A3, epsilon):
    print("                                          Punctul 1 al problemei!")
    print("Matrix 1 informations ")
    show_information_for_p1(A1, epsilon)
    print(
        "-------------------------------------------------------------------------------------------------------------------------------------")

    print("Matrix 3 information ")
    show_information_for_p1(A3, epsilon)
    print(
        "-------------------------------------------------------------------------------------------------------------------------------------")

def point2(A, epsilon):
    k=0
    k_max = 100000
    P, L, U = lu(A)
    L = np.matrix(L)
    index = 1
    diferenta = 1
    while np.linalg.norm(diferenta) > epsilon and k < k_max:
        for i in range(index):
            L = L * L
        L_transpose = L.transpose()
        A_first = L *L_transpose
        A_second = L_transpose * L
        A_first_matrix = np.matrix(A_first)
        A_second_matrix = np.matrix(A_second)
        diferenta = np.linalg.norm(abs(A_first_matrix - A_second_matrix))
        index += index
    print("                                          Punctul 2 al problemei!")
    print("Diferenta dintre A(k) si A(k+1): ")
    print(diferenta)
    print("A(k): ")
    print(A_first_matrix)
    print(
        "-------------------------------------------------------------------------------------------------------------------------------------")
#cazul p > n --------------------------------------------------------------------------------------------------------------------------------------------------------
def point3(A, p, n):
    print("                                          Punctul 3 al problemei!")

    U, s, VT = svd(A)
    print("Valorile singulare ale matricei A: ")
    print(s)
    print()

    print("Rangul matricei A este: ")
    A_prim = matrix(A)
    #numarul de valori singulare strict pozitive se poate calcula rangul si aplicand "len()" pe s.
    print(np.linalg.matrix_rank(A_prim))
    print()

    print("Numarul de conditionare al matricei A:")
    min_value = min(s)
    max_value = max(s)
    print(max_value / min_value)
    print()

    print("Pseudoinversa Moore-Penrose a matricei A: ")
    S_I = calculate_S_I(s, p, n)
    S_I = np.array(S_I, dtype= np.float)
    UT = U.transpose()
    V = VT.transpose()
    UT = np.array(UT, dtype = np.float)
    V = np.array(V, dtype = np.float)
    A_I =V.dot(S_I).dot(UT)
    print(A_I)
    print()

    print("Matricea pseudo-inversa in sensul celor mai mici patrate: ")
    A_T = A.transpose()
    A_J = np.linalg.inv((A_T.dot(A))).dot(A_T)
    print(A_J)
    norma = np.linalg.norm(abs(A_I - A_J))
    print("Norma este: ", np.float(norma))

#partea bonus
def bonus_Jacobi(v, n, epsilon):
    l=0
    l_max = 100000
    U = np.identity(n)
    p, q, k = bonus_calculate_p_and_q(v, n)
    alfa = bonus_calculate_alfa(v, n, p, q, k)
    s, c, t = calculate_SCT(alfa)
    while abs(v[k]) > epsilon and l <= l_max:
        v = bonus_calculate_matrixA_rotation(v,p,q,c,s,t,k,n)
        U = recalculate_U(U,p,q,c,s)
        p, q, k = bonus_calculate_p_and_q(v, n)
        alfa = bonus_calculate_alfa(v,n,p,q,k)
        s, c, t = calculate_SCT(alfa)
        l += 1
    print("Lambda: ")
    print(np.round(v, 6))

def bonus_calculate_p_and_q(v,n):
    i = 1
    j = 0
    k = 1
    max_value = 0
    while i <= n:
        j= 0
        while j < i:
            if abs(v[k]) > max_value:
                max_value = abs(v[k])
                p = i
                q = j
                k_ramas = k
            j += 1
            k = k + 1
        k += 1
        i += 1

    return p, q, k_ramas

def bonus_calculate_alfa(v, n, p, q, k):
    i = 0
    j = 0
    l = 0
    while i <= n:
        j = 0
        while j <= i:
            if i == j and i == p:
                pp = v[l]
            if i==j and i == q:
                qq = v[l]
            j += 1
            l = l + 1
        i += 1
    #print(pp,     "        ", qq, "     ",v[k])
    return (np.float(pp) - np.float(qq)) / np.float(2*v[k])

def bonus_calculate_matrixA_rotation(v, p, q, c, s, t, k, n):
    i = 0
    j = 0
    l = 0
    while i <= n:
        j = 0
        while j <= i:
            if i != j:
                try:
                    v[get_position(p, i, n)] = (c * v[get_position(p, i, n)]) + (s * v[get_position(q, i, n)])
                    v[get_position(i, q, n)] = (-s * v[get_position(j, p, n)]) + (c * v[get_position(q, j, n)])
                except:
                    print("")
            try:
                v[get_position(p, p, n)] = v[get_position(p, p, n)] + (t * v[get_position(p, q, n)])
                v[get_position(q, q, n)] = v[get_position(q, q, n)] - (t * v[get_position(p, q, n)])
            except:
                print("")
            j += 1
        v[k] = 0
        i += 1
    return v

def get_position(x, y, n):
    i = 0
    j = 0
    l = 0
    while i <= n:
        j = 0
        while j <= i:
            if i == x and j == y:
                return l
            j += 1
            l += 1
        i += 1


if __name__ == "__main__":
    A1 = np.array([
        [1, 1, 2],
        [1, 1, 2],
        [2, 2, 2]
    ], dtype = np.float)
    A2 = np.array([
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1 ,0, 1, 0],
        [0, 1, 0, 1]
    ], dtype = np.float)
    A3 = np.array([
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6],
        [4, 5, 6, 7]
    ], dtype = np.float)
    A4 = np.array([
        [4, 5, 2, 2],
        [1, 3, 2, 1],
        [5, 3, 6, 1],
        [9, 3, 5, 7],
        [1, 2, 4, 6]
    ], dtype = np.float)
    epsilon = 0.0000001
    point1(A1, A2, A3, epsilon)
    point2(A1, epsilon)
    p = 5
    n = 4
    point3(A4, p, n)
    #v = [1, 2, 3, 3, 4, 5, 4, 5, 6, 7]
    v = [-1.16515139e+00, -2.91792980e-15, -2.01703507e-16, -3.02965995e-15,7.41228128e-16, 6.30969607e-16, 9.97803589e-09,  0.00000000e+00,  2.16761261e-22,  1.71651514e+01]
    #v = [1,1,1,2,2,2]
    print("---------------------------------------------------------------------------------------------------------------------")
    """
    p, q, k = bonus_calculate_p_and_q(v,3)
    alfa = calculate_alfa(A3,p,q)
    s, c,t = calculate_SCT(alfa)
    a = calculate_matrixA_rotation(A3,p,q,c,s,t)
    v1 = bonus_calculate_matrixA_rotation(v,p,q,c,s,t,k,3)
    print(a)
    """
    print("                                        Partea bonus")
    bonus_Jacobi(v,3,epsilon)




