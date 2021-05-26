import numpy as np
#citeste matricile de rare de forma celei din fisier
def read_matrix_A(file_path):
    f = open(file_path, 'rb')
    size=int(f.readline().strip())
    vector=[[''for i in range(0)] for j in range(size)]
    a=[]
    lines=f.readlines()
    index=2
    for i in lines:
        if index>2:
            value = (float)(i.strip().decode().replace(",", "").split(" ")[0])
            line = (int)(i.strip().decode().replace(",", "").split(" ")[1])
            col = (int)(i.strip().decode().replace(",", "").split(" ")[2])
            size_line = len(vector[line])
            for j in range(size_line):
                if col == (vector[line][j][1]):
                    value+=vector[line][j][0]
                    #print("sunt si elemente duble")
            vector[line].append([value,col])

        index+=1
    for i in range(size):
        a.append(vector[i])
    #print(a)
    return a

#citeste si stocheaza matricile de tipul celei din fisierul b.txt
def read_matrix_B(file_path):
    f = open(file_path, 'rb')
    lines = f.readlines()
    a=[]
    b=[]
    c=[]
    matrix_B=[]
    for i in lines:
        matrix_B.append(i.strip().decode())
    size=(matrix_B[0])
    p=(matrix_B[1])
    q=(matrix_B[2])
    matrix_B.remove(size)
    matrix_B.remove(p)
    matrix_B.remove(q)
    matrix_B.remove('')
    size=int(size)
    p=int(p)
    q=int(q)
    for i in range(size):
        a.append((float)(matrix_B[i]))
    for i in range(size+1,(size+size-p+1)):
        b.append((float)(matrix_B[i]))
    for i in range((size+size-p+1)+1,(size+size-p+1)+(size-q+1)):
        c.append((float)(matrix_B[i]))
    return (a,b,c,p,q)


#functia unde calculez matricea A+B
def aplusb(matrix_a,a,b,c,p,q):
    matrix_sum = [['' for i in range(2)] for j in range(2021)]
    ramura_else=False
    for i in range(len(matrix_a)):
        matrix_sum[i].remove('')
        matrix_sum[i].remove('')
        ramura_else=False
        size_cel = len(matrix_a[i])
        for j in range(size_cel):
            if int(matrix_a[i][j][1]) == i:
                value = (float)(matrix_a[i][j][0]) + a[i]
                index = (int)(matrix_a[i][j][1])
                matrix_sum[i].append([value, index])
            elif int(matrix_a[i][j][1]) - i == q:
                value = (float)(matrix_a[i][j][0]) + b[i]
                index = (int)(matrix_a[i][j][1])
                matrix_sum[i].append([value, index])
            elif i - int(matrix_a[i][j][1]) == p:
                value = (float)(matrix_a[i][j][0]) + c[i-1]
                index = (int)(matrix_a[i][j][1])
                matrix_sum[i].append([value, index])
            else:
                value = (float)(matrix_a[i][j][0])
                index = (int)(matrix_a[i][j][1])
                matrix_sum[i].append([value, index])
                ramura_else=True
        if ramura_else==True:
            if i < 2020:
                value = float(b[i])
                index = i + 1
                #if [value,index] not in matrix_a[i+1]:
                if verificare(matrix_sum[i],index)==False:
                      matrix_sum[i].append([value, index])
            if i>0 and i<2021:
                value = float(c[i-1])
                index = i - 1
                if verificare(matrix_sum[i],index) == False:
                    matrix_sum[i].append([value,index])
    #print(matrix_sum[0])
    #print(b)
    return matrix_sum

#o functie ce ma ajuta s aimi dau seama daca nu adaug elemente in plus in matricea aplusb..
def verificare(m,index):
    for i in m:
        if i[1] == index:
            return True
    return False

#functia unde imi calculez pentru o linie din matricea A produsul elementele pentru ptima linie din matricea AxB
def multiplication(m_a,a,b,c):
    new_v=[]
    sum=0
    for i in range(2021):
        coloana=i
        for j in m_a:
            if coloana == j[1]:
                #print(j[0],a[coloana])
                sum += float(j[0]) * a[coloana]
            elif coloana == j[1] - 1:
                sum += float(j[0]) * c[coloana]
            elif coloana == j[1] + 1:
                sum += float(j[0]) * b[coloana-1]
        if sum!=0:
            new_v.append([sum,coloana])
        sum = 0
    #print("Matricea rezultat :",new_v)
    return new_v


def print_result_axb(matrix_aorib,m_aorib):
    message=False
    while message == False:
        index=int(input("Introduceti un index pentru a compara rezultatul inmultirii cu ce trebuia de fapt sa calculeze: "))
        if index >0 and index <2021:
            message=True
            matrix_aorib[index].sort(key=sort_func)
            m_aorib[index].sort(key=sort_func)
            print("Matricea: ",matrix_aorib[index])
            print("Rezultat: ",m_aorib[index])
        else:
            print("Nu ati introdus un numar valid!!!")

def sort_func(e):
    return e[1]

def sort_matrix(m):
    sorted_m=[]
    for i in range(len(m)):
            m[i].sort(key=sort_func)
            sorted_m.append(m[i])
    return sorted_m



def bonus(a,b,c):
    matrix=[]
    matrix_t=[]
    for i in range(2021):
        if i==0:
                #print("sunt aici")
                matrix.append([a[i],i])
                matrix.append([b[i],i+1])
                matrix_t.append(matrix)
        elif i>0 and i<2020:
                matrix.append([c[i-1],i-1])
                matrix.append([a[i],i])
                matrix.append([b[i],i+1])
                matrix_t.append(matrix)
        else:
                matrix.append([a[i],i])
                matrix_t.append(matrix)
        matrix=[]
    return matrix_t

def bonus2(a,b,c,x,y,z):
    matrix=[]
    matrix_t=[]
    for i in range(len(a)):
        if i == 0:
            matrix.append((a[i]*x[i])+(b[i]*z[i]))
            matrix.append((a[i]*y[i])+(b[i]*x[i+1]))
            matrix.append(b[i]*y[i+1])
            matrix_t.append(matrix)
        elif i==1:
            matrix.append((c[i-1]*x[i-1])+(a[i]*z[i-1]))
            matrix.append((c[i-1]*y[i-1])+(a[i]*x[i])+(b[i]*z[i]))
            matrix.append((a[i]*y[i])+(b[i]*x[i+1]))
            matrix.append((b[i]*y[i+1]))
            matrix_t.append(matrix)
        elif i==2 and len(a)<5:
            matrix.append(c[i-1]*z[i-2])
            matrix.append((c[i-1]*x[i-1])+(a[i]*z[i-1]))
            matrix.append((c[i-1]*y[i-1])+(a[i]*x[i])+(b[i]*z[i]))
            matrix.append((a[i-1]*y[i-1])+(b[i-1]*x[i]))
            matrix_t.append(matrix)
        elif i>1 and i<len(a)-1:
            matrix.append(c[i - 1] * z[i - 2])
            matrix.append((c[i - 1] * x[i - 1]) + (a[i] * z[i - 1]))
            matrix.append((c[i - 1] * y[i - 1]) + (a[i] * x[i]) + (b[i] * z[i]))
            matrix.append((a[i - 2] * y[i]) + (b[i] * z[i]))
            matrix.append(b[i]*z[i])
            matrix_t.append(matrix)
        elif i==len(a)-1:
            matrix.append((c[i-1]*z[i-2]))
            matrix.append((c[i-1]*x[i-1])+(a[i]*z[i-1]))
            matrix.append((c[i-1]*y[i-1])+a[i]*x[i])
            matrix_t.append(matrix)
        matrix=[]
    return matrix_t

def transformIntoMatrixD(a,b,c,p,q, i):
    m = []
    m2 =[]
    for j in range(len(a)):
        if j == i:
            m.append(a[i])
        elif i-j==q:
            m.append(b[i])
        elif j-i==p:
            m.append(c[i])
        else:
            m.append(0)

    return m
def problemaBonusPrincipala(a,b,c,x,y,z,p,q,p1,q1):
    n=len(a)
    a1=[0,-1]
    b1=[0,-2]
    c1=[0,-3]
    x1=[0,-4]
    y1=[0,-5]
    z1=[0,-6]
    m=[]
    m1=[]
    m2=[]

    for i in range(n):
        sum=0
        for j in range(n):
            if i==0:
                if i == j:
                    a1 = [a[i], j]
                elif j - i == q:
                    b1 = [b[i], j]
            if i>0 and i<n-1:
                if i == j:
                    a1 = [a[i], j]
                elif j - i == q:
                    b1 = [b[i], j]
                elif i - j == p:
                    c1 = [c[i-1], j]
            if i == n-1:
                if i == j:
                    a1 = [a[i], j]
                elif i - j == p:
                    c1 = [c[i-1], j]
                b1=[0,-2]
        if a1[1]>=0 and b1[1]>=0 and c1[1]>=0:
            m1.append([a1,b1,c1])
        elif a1[1]>=0  and b1[1]>=0:
            m1.append([a1,b1])
        elif a1[1]>=0 and c1[1]>=0:
            m1.append([a1,c1])

        #print(a1,"   ",b1,"   ",c1)
        for k in range(n):
            if i<p1:
                if i == k:
                    x1 = [x[i], k]
                elif k - i == p1:
                    z1 = [z[i], k]
            elif i>=p1 and i<n-p1:
                if i == k:
                    x1 = [x[i], k]
                elif k - i == p1:
                    z1 = [z[i], k]
                elif i - k == q1:
                    y1 = [y[i-p1],k]
            elif i>=n-p1:
                if i == k:
                    x1 = [x[i], k]
                elif i - k == q1:
                    y1 = [y[i - p1], k]
                z1=[0,-1]
        #print(x1, y1, z1)
        if x1[1]>=0 and y1[1]>=0 and z1[1]>=0:
            m2.append([x1,y1,z1])
        elif x1[1]>=0  and y1[1]>=0:
            m2.append([x1,y1])
        elif x1[1]>=0 and z1[1]>=0:
            m2.append([x1,z1])
        """
                   if a1[1] == x1[1]:
               sum += a1[0] * x1[0]
           if a1[1] == y1[1]:
               sum += a1[0] * y1[0]
           if b1[1] == z1[1]:
               sum += b1[0] * z1[0]
           if c1[1] == x1[1]:
               sum += b1[0] * x1[0]
           if b1[1] == x1[1]:
               sum += b1[0]*x1[0]
           m.append(sum)
        """
    m1=sort_matrix(m1)
    m2=sort_matrix(m2)
    sum=0
    for i in m1:
        for j in m2:
            for k in i:
                for l in j:
                    if k[1]==l[1]:
                        sum+=k[0]*l[0]
            m.append(sum)
            sum=0
    for ind in range(len(m1)):
        print(m1[ind])
    print("________________________________")
    for ind1 in range(len(m2)):
        print(m2[ind1])

    print("mat Rezultat: ",m)
if __name__ == '__main__':
    contor=0
    file_path_a = "a.txt"
    file_path_b = "b.txt"
    file_path_aorib="aorib.txt"
    file_path_aplusb="aplusb.txt"
    matrix_a = read_matrix_A(file_path_a)
    matrix_aorib = read_matrix_A(file_path_aorib)
    matrix_aplusb = read_matrix_A(file_path_aplusb)
    #print(matrix_a[0])
    ramura_else = False
    a, c, b, p, q = read_matrix_B(file_path_b)
    m_aorib = []
    for i in matrix_a:
        m_aorib.append(multiplication(i, a, b, c))
    m_aplusb=aplusb(matrix_a, a, b, c, p, q )
    m_aplusb = sort_matrix(m_aplusb)
    matrix_aplusb = sort_matrix(matrix_aplusb)
    matrix_aorib = sort_matrix(matrix_aorib)
    m_aorib = sort_matrix(m_aorib)
    if m_aplusb==matrix_aplusb:
        print("Matricea A+B este aceasi cu cea din fisierul aplusb.txt")
    for i in range(len(matrix_aplusb)):
        if matrix_aplusb[i]!=m_aplusb[i]:
              print(i)
    if m_aorib == matrix_aorib:
        print("Matricia AxB este aceasi cu cea din fisierul aorib.txt")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print_result_axb(matrix_aplusb, m_aplusb)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print_result_axb(matrix_aorib,m_aorib)
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    a1=[1,2,2,2,5]
    b1=[2,1,3,3]
    c1=[3,2,1,2]
    x1=[3,5,2,1,2]
    y1=[3,2,2]
    z1=[1,2,3]
    #mt=transformIntoMatrixD(x1,y1,z1,2,2,3)
    problemaBonusPrincipala(a1,b1,c1,x1,y1,z1,1,1,2,2)













    #prima incercare pentru partea bonus!
    """
    a1=[1,3,1,1]
    b1=[2,4,2]
    c1=[2,1,2]
    m=[[1,0],[2,1]]
    print(bonus(m,a1,b1,c1))
    B_transformat=bonus(a,c,b)
    BxB=[]
    for i in B_transformat:
        BxB.append(multiplication(i,a,c,b))
    BxB2=bonus2(a,c,b,a,c,b)
    print("Folosind ambele metode implementate pentru problema bonus comparam rezultatele!")
    while True:
        pos=int(input("Introduceti o pozitie: "))
        if pos>=0 and pos<2021:
            break
        else:
            "Introduceti o pozitie valida!!!"
    print("Prima metoda",BxB[pos])
    print("A doua metoda",BxB2[pos])
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    matricea_simpla1=[
        [1 ,2 ,0, 0],
        [2 , 2, 1,0],
        [0, 1, 3, 1],
        [0, 0, 2, 1]
    ]
    matricea_simpla2=[
        [3, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 2, 2, 1],
        [0, 0, 1, 1]
    ]
    print("Avem aceste 2 matrici simple: ")
    print(matricea_simpla1)
    print(matricea_simpla2)
    print("Rezultatul inmultirii celor 2 matrici folosind implementarea bonusului ")
    a1=[1,2,3,1]
    b1=[2,1,1]
    c1=[2,1,2]
    x=[3,1,2,1]
    y=[1,1,1]
    z=[1,2,1]
    a2=[1,1,1,2,1,1,1]
    c2=[1,1,2,1,1,2]
    b2=[1,2,2,1,1,2]
    x1=[2,1,1,2,1,1,2]
    y1=[1,1,2,2,1,1]
    z1=[1,1,2,1,1,2]
    rez=bonus2(a1,b1,c1,x,y,z)
    print(rez)
    rez2=bonus2(a2,b2,c2,x1,y1,z1)
    print(rez2)
    """
