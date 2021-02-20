
def problema1():
    u=0
    puterea=0
    for i in range(0,20):
        u=pow(10,-i)
        if 1.0+u==1.0:
            puterea=i-1 #eu dau break atunci cand conditia din if este adevarata dar am nevoie de acel numar de dinainte care nu respecta conditia prezentata in if.
            break
    return pow(10,-puterea)

#-------------------------------------------------------------------------------------------------------------------
#Mai trebuie sa gasesc ex=xemlul pentru inmultire
def problema2():
    u=problema1()
    a=1.0
    b=u/10
    c=u/10
    calcul1=(a+b)+c
    calcul2=a+(b+c)
    if calcul1 != calcul2:
        print("Operatia nu este asociativa")
    else:
        print("Operatia este asociativa")

#---------------------------------------------------------------------------------------------------------------------
def problema3_Lentz(x,epsilon):
   a=x; b=0
   f=b; mic=pow(10,-12)
   if f==0:
       f=mic
   C=f
   D=0
   j=1
   while True:
       a = -pow(x, 2)
       b = (2 * j) - 1
       D = b + a * D
       if D == 0:
           D = mic
       C = b + a / C
       if C == 0:
           C = mic
       D = 1 / D
       delta = C * D
       f = delta * f
       j = j + 1
       if abs(delta-1) < epsilon:
          b = (2 * j) - 1
          D = b + a * D
          if D == 0:
              D = mic
          C = b + a / C
          if C == 0:
              C = mic
          D = 1 / D
          delta = C * D
          f = delta * f
          j = j + 1
          break
   print(f)
if __name__ == '__main__':
    u=problema1()
    print("Problema1 : ",u)
    problema2()
    pi=3.141593
    problema3_Lentz(0.2,1.11022302462515654042E-16)

