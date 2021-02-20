import math
import random as r
import time
import pygame as p

def problema1():
    u = 0
    puterea = 0
    for i in range(0, 20):
        u = pow(10, -i)
        if 1.0 + u == 1.0:
            puterea = i - 1  # eu dau break atunci cand conditia din if este adevarata dar am nevoie de acel numar de dinainte care nu respecta conditia prezentata in if.
            break
    return pow(10, -puterea)


# -------------------------------------------------------------------------------------------------------------------
# Mai trebuie sa gasesc ex=xemlul pentru inmultire
def problema2():
    u = problema1()
    a = 1.0
    b = u / 10
    c = u / 10
    calcul1 = (a + b) + c
    calcul2 = a + (b + c)
    if calcul1 != calcul2:
        return True
    else:
        return False
#partea a 2 a a problemei
def problema2_inmultirea():
    u = problema1()
    a = 1.0
    b=u/10
    c=u/10
    conditie=(a * b) * c == a * (b * c)
    while conditie:
        a=a*1.1
        conditie=(a * b) * c == a * (b * c)
    exemplu="( "+str(a)+" * "+str(b)+ ") *"+ str(c)+" != "+str(a)+" * ("+str(b)+" * "+str(c)+")."
    pas1=(a * b) * c
    pas2=a * (b * c)
    return(exemplu,pas1,pas2)
# ---------------------------------------------------------------------------------------------------------------------
def problema3_Lentz(x, epsilon):
    a = x
    b = 0
    f = b
    mic = pow(10, -12)
    if f == 0:
        f = mic
    C = f
    D = 0
    j = 1
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
    while abs(delta - 1) >= epsilon:
        a = -x ** 2
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
    return f

def problema3_Polinoame(x):
    c1 = 0.33333333333333333
    c2 = 0.133333333333333333
    c3 = 0.053968253968254
    c4 = 0.0218694885361552
    x3=pow(x,3)
    x5=pow(x,5)
    x7=pow(x,7)
    x9=pow(x,9)
    tan=x+c1*x3+c2*x5+c3*x7+c4*x9
    return tan

#facem un generator de 10000 de numere pentru a calcula tangenta cu Lentz
def generator():
    numbers=[0 for i in range(0,10000)]
    count=0
    while(count<10000):
        number=r.random()
        if number not in numbers:
            numbers.append(number)
            count=count+1
    return numbers

#functia ce calculeaza mediile pentru tangente folosind tangenta prin metoda Lentz
def avg_Lentz(epsilon,numbers):
    sum_Lentz=0
    sum_tan=0
    start=time.time()
    for i in numbers:
        sum_Lentz+=problema3_Lentz(i,epsilon)
        sum_tan+=math.tan(i)
    finish=time.time()
    seconds=finish-start
    return (sum_Lentz/10000,sum_tan/10000,seconds)
#functia ce calculeaza media pentru tangeta folosind tangenta prin metoda polinoamelor
def avg_Polinom(numbers):
    sum_Pol=0
    sum_tan=0
    start=time.time()
    for i in numbers:
        sum_Pol+=problema3_Polinoame(i)
        sum_tan+=math.tan(i)
    finis=time.time()
    seconds=finis-start
    return(sum_Pol/10000,sum_tan/10000,seconds)


def prob1_interface(mesaj1,mesaj2,index_prob):
    p.init()
    size_x = 600
    size_y = 400
    p1= p.display.set_mode((size_x, size_y))
    color1="white"
    font_titlu=p.font.Font('freesansbold.ttf', 30)
    font=p.font.Font('freesansbold.ttf', 20)
    fontp3=p.font.Font('freesansbold.ttf', 17)
    font_mic=p.font.Font('freesansbold.ttf', 9)
    flag=False
    titlu=""
    if index_prob==1:
        titlu="Problema 1"
    elif index_prob==2:
        titlu="Problema 2"
        mesaj_conditie,pas1,pas2=problema2_inmultirea()
        conditie=str(pas1)+" != "+str(pas2)+"."
    elif index_prob==3:
        titlu="Problema 3"
        mesaj1 = "Lentz (eroare): " + str(mesaj1)
        mesaj2 = "Polinom (erroare): "+str(mesaj2)

    while(flag==False):
        p.display.set_caption(titlu)
        p.display.flip()
        bk = p.image.load("bck222.jpg")
        bk = p.transform.scale((bk), (size_x, size_y))
        p1.blit(bk, p.Rect(0, 0, 400, 400))
        for events in p.event.get():
            if events.type == p.QUIT:
                return "close"
        title = font_titlu.render(titlu, True, "red", (0, 0, 0))
        titleRect = title.get_rect()
        titleRect.center = (300, 50)
        if index_prob==1:
            text_box1 = font.render(mesaj1, True, color1, (0, 0, 0))
            textRect1 = text_box1.get_rect()
            textRect1.center = (310, 200)

            text_box2 = font.render(mesaj2, True, color1, (0, 0, 0))
            textRect2 = text_box1.get_rect()
            textRect2.center = (300, 235)

            p1.blit(text_box2, textRect2)
            p1.blit(text_box1, textRect1)
        elif index_prob==3:
            text_box1 = fontp3.render(mesaj1, True, color1, (0, 0, 0))
            textRect1 = text_box1.get_rect()
            textRect1.center = (300, 150)

            text_box2 = font_titlu.render("VS", True, color1, (0, 0, 0))
            textRect2 = text_box2.get_rect()
            textRect2.center = (300, 225)

            text_box3 = fontp3.render(mesaj2, True, color1, (0, 0, 0))
            textRect3 = text_box3.get_rect()
            textRect3.center = (300, 300)


            p1.blit(text_box1, textRect1)
            p1.blit(text_box2, textRect2)
            p1.blit(text_box3, textRect3)
        elif index_prob==2:
            text_box1 = font.render(mesaj1, True, color1, (0, 0, 0))
            textRect1 = text_box1.get_rect()
            textRect1.center = (310, 200)

            text_box2 = font.render(mesaj2, True, color1, (0, 0, 0))
            textRect2 = text_box1.get_rect()
            textRect2.center = (300, 235)

            text_box3 = font_mic.render(mesaj_conditie,True,color1,(0,0,0,0))
            textRect3 = text_box3.get_rect()
            textRect3.center = (300,300)

            text_box4 = fontp3.render(conditie,True,color1,(0,0,0,0))
            textRect4 = text_box4.get_rect()
            textRect4.center = (300,350)

            p1.blit(text_box2, textRect2)
            p1.blit(text_box1, textRect1)
            p1.blit(text_box3,textRect3)
            p1.blit(text_box4,textRect4)
        p1.blit(title,titleRect)

def menu_interface():
    p.init()
    size_x_menu = 600
    size_y_menu = 400
    meniu = p.display.set_mode((size_x_menu, size_y_menu))
    color1 = "white"
    color2 = "white"
    color3 = "white"
    color4 = "white"
    font_titlu = p.font.Font('freesansbold.ttf', 60)
    font_menu = p.font.Font('freesansbold.ttf', 30)
    flag = False
    flag_prob1 = False
    flag_prob2 = False
    flag_prob3 = False
    flag_exit = False

    # partea de interfata grafica
    while (flag == False):
        p.display.set_caption("Tema1")
        # efectul de butoane adevarate
        mouse_x, mouse_y = p.mouse.get_pos()
        if mouse_x > 210 and mouse_x < 390 and mouse_y > 140 and mouse_y < 160:
            color1 = "blue"
            color2 = "white"
            color3 = "white"
            color4 = "white"
        elif mouse_x > 210 and mouse_x < 390 and mouse_y > 190 and mouse_y < 210:
            color2 = "blue"
            color1 = "white"
            color3 = "white"
            color4 = "white"
        elif mouse_x > 210 and mouse_x < 390 and mouse_y > 240 and mouse_y < 260:
            color3 = "blue"
            color1 = "white"
            color2 = "white"
            color4 = "white"
        else:
            color2 = "white"
            color1 = "white"
            color3 = "white"
            color4 = "white"
        # forul cu evenimente ce apar pe interfata grafica
        for events in p.event.get():
            if events.type == p.QUIT:
                flag = True
                flag_prob1 = False
                flag_prob2 = False
                flag_prob3 = False
            elif events.type == p.MOUSEBUTTONDOWN:
                coordonata_x, coordonata_y = p.mouse.get_pos()
                if coordonata_x > 210 and coordonata_x < 390 and coordonata_y > 140 and coordonata_y < 160:
                    flag_prob1 = True
                    flag_prob2 = False
                    flag_prob3 = False
                    flag=True
                elif coordonata_x > 210 and coordonata_x < 390 and coordonata_y > 190 and coordonata_y < 210:
                    flag_prob1 = False
                    flag_prob2 = True
                    flag_prob3 = False
                    flag = True
                elif coordonata_x > 210 and coordonata_x < 390 and coordonata_y > 240 and coordonata_y < 260:
                    flag_prob1 = False
                    flag_prob2 = False
                    flag_prob3 = True
                    flag = True

        bk_menu = p.image.load("bck222.jpg")
        bk_menu = p.transform.scale((bk_menu), (size_x_menu, size_y_menu))
        meniu.blit(bk_menu, p.Rect(0, 0, 400, 400))

        # butoane pentru probleme
        title = font_titlu.render("TEMA 1", True, "red", (0, 0, 0))
        titleRect = title.get_rect()
        titleRect.center = (300, 50)
        menu1 = font_menu.render("Problema 1", True, color1, (0, 0, 0))
        menu1Rect = menu1.get_rect()
        menu1Rect.center = (300, 150)
        menu2 = font_menu.render("Problema 2", True, color2, (0, 0, 0))
        menu2Rect = menu2.get_rect()
        menu2Rect.center = (300, 200)
        menu3 = font_menu.render("Problema 3", True, color3, (0, 0, 0))
        menu3Rect = menu3.get_rect()
        menu3Rect.center = (300, 250)
        meniu.blit(title, titleRect)
        meniu.blit(menu1, menu1Rect)
        meniu.blit(menu2, menu2Rect)
        meniu.blit(menu3, menu3Rect)
        p.display.flip()
    return (flag_prob1,flag_prob2,flag_prob3)

if __name__ == '__main__':
    pi = 3.141593
    epsilon = 1.11022302462515654042E-16
    numbers = generator()
    flag_prob1,flag_prob2,flag_prob3=menu_interface()
    while(True):
        if flag_prob1 == True:
            u = problema1()
            #print("Problema1 : ", u)
            mesaj1="Rezolvare: cel mai mic numar u pentru care 1.0 + u != 1.0 "
            mesaj2="este numarul: "+str(u)+"."
            flag_prob1,flag_prob2,flag_prob3=(False,False,False)
            mesaj_primit=prob1_interface(mesaj1,mesaj2,1)
            if mesaj_primit=="close":
                flag_prob1, flag_prob2, flag_prob3=menu_interface()
        elif flag_prob2 == True:
            if problema2()==True:
                mesaj1="Rezolvare: Operatia de adunare (a + b) + c != a + (b + c)"
                mesaj2="nu este asociativa."
            else:
                mesaj1 = "Rezolvare: Operatia de adunare (a + b) + c != a + (b + c)"
                mesaj2 = " este asociativa."
            flag_prob1, flag_prob2, flag_prob3 = (False, False, False)
            mesaj_primit = prob1_interface(mesaj1, mesaj2,2)
            if mesaj_primit == "close":
                flag_prob1, flag_prob2, flag_prob3 = menu_interface()
        elif flag_prob3 == True:
            # pentru Lentz
            avg_L, avg_tan, seconds_Lentz = avg_Lentz(epsilon, numbers)
            error_Lentz = abs(avg_tan - avg_L)
            #print("(Metoda Lentz)Eroare este de :", error_Lentz, " calculata in ", seconds_Lentz, " secunde")
            mesaj1=str(error_Lentz)+" , timp:"+str(seconds_Lentz)+" s."

            # pentru metoda polinomiala
            avg_P, avg_tan, seconds_Pol = avg_Polinom(numbers)
            error_Pol = avg_tan - avg_P
            #print("(Metoda polinomiala)Eroarea este de: ", error_Pol, " calculata in ", seconds_Pol, " secunde")
            mesaj2=str(error_Pol)+" , timp:"+str(seconds_Pol)+" s."
            flag_prob1, flag_prob2, flag_prob3 = (False, False, False)
            mesaj_primit = prob1_interface(mesaj1, mesaj2, 3)
            if mesaj_primit == "close":
                flag_prob1, flag_prob2, flag_prob3 = menu_interface()
        else:
            break

    problema2_inmultirea()



