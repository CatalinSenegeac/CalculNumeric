def Olver_method(x_list, coef, epsilon):
    seeds = []
    k_max = 10000
    R = calculate_R(coef)
    index = -R

    while index <= R:
        k = 0
        x = index
        delta_x = calculate_deltaX(x, x_list, coef)
        x = x - delta_x
        k += 1
        while abs(delta_x) >= epsilon and k <= k_max and abs(delta_x) <= pow(10, 8):
            d_x_list, d_coef = calculate_polinom_derivate(x_list, coef)
            if abs(len(d_coef)) < epsilon:
                exit("it came out of Olver's method..")
            delta_x = calculate_deltaX(x, x_list, coef)
            x = x - delta_x
            k += 1
        if abs(delta_x) < epsilon:
            seeds.append(x)
        else:
            print("divergence, try to change x0 ..")
        index += 0.1
    return seeds

def calculate_R(coef):
    a0 = coef[0]
    A = max(coef)
    R = (a0 + A) / a0
    return R

def calculate_polinom_derivate(x_list, coef):
    d_coef = []
    d_x_list = []
    for i in range(len(x_list)):
        if coef[i] * x_list[i] != 0:
              d_coef.append(coef[i] * x_list[i])
        if x_list[i] - 1 >= 0:
            d_x_list.append(x_list[i] - 1)
    return (d_x_list, d_coef)

def calculate_deltaX(x, x_list, coef):
    #p_xk = calculate_Px(x, x_list, coef)
    p_xk = Horner(x, x_list, coef)
    x_listd1, coefd1 = calculate_polinom_derivate(x_list, coef)
    #p1_xk = calculate_Px(x, x_listd1, coefd1)
    p1_xk = Horner(x, x_listd1,coefd1)
    ck = calculate_ck(x,x_list,coef)

    try:
        delta_x = (p_xk / p1_xk) + (0.5 * ck)
    except:
        print("(deltaX) divided by 0 exception .. ")
    return delta_x

def calculate_ck(x, x_list, coef):
    x_listd1, coefd1 = calculate_polinom_derivate(x_list, coef)
    x_listd2, coefd2 = calculate_polinom_derivate(x_listd1, coefd1)
    #p_xk = calculate_Px(x, x_list, coef)
    p_xk = Horner(x, x_list, coef)
    p_xk = p_xk ** 2

    #p1_xk = calculate_Px(x, x_listd1, coefd1)
    p1_xk = Horner(x, x_listd1, coefd1)
    p1_xk = p1_xk ** 3

    #p2_xk = calculate_Px(x, x_listd2, coefd2)
    p2_xk = Horner(x, x_listd2, coefd2)

    try:
        result = (p_xk * p2_xk) / p1_xk
    except:
        print("(Ck) divided by 0 exception ..")
    return result

def calculate_Px(x, x_list, coef):
    x_values = 0
    for i in range(len(x_list)):
        x_values += ( coef[i] * (x**(len(x_list)-1-i)))
    print(x_values)
    return x_values

def Horner(x, x_list, coef):
    b0 = coef[0]
    i=1
    n = len(coef)
    while i < n:
        b0 = coef[i] + b0 * x
        i+=1
    #print (b0)
    return b0

def drop_same_seeds(seeds, epsilon):
    optim_seeds = []
    seeds.sort()
    for i in range(len(seeds)-1):
        if abs(seeds[i] - seeds[i+1]) > epsilon:
            optim_seeds.append(seeds[i])
    return optim_seeds

if __name__ == '__main__':
    epsilon = 0.00000000000001
    coef = [1, -6, 11, -6]
    x_list = [3, 2, 1 , 0]
    seeds = Olver_method(x_list, coef, epsilon)
    optim_seeds = drop_same_seeds(seeds, epsilon)
    optim_seeds.append(seeds[len(seeds)-1])
    print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    print("Radacinile gasite de catre algoritm: ")
    print(seeds)
    print()
    print("Radacinile polinomului sunt: ")
    print(optim_seeds)

    f = open("radacini.txt", "w")
    for i in optim_seeds:
        f.write(str(i)+", ")
    f.close()