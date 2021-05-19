from tkinter.constants import X
import PySimpleGUI as sg
import numpy as np
import pygame
from time import time, sleep
from random import randint as r
import random
import matplotlib.pyplot as plt
import math

class Form:
    #Bilgileri aldigimiz form sayfasi
    def FormPage(self):
        sg.theme('LightGrey 6')     
        layout = [
            [sg.Text('Please enter information')],
            [sg.Text('Start Location', size =(15, 1)), sg.InputText()],
            [sg.Text('Finish Location', size =(15, 1)), sg.InputText()],
            [sg.Text('Matrix Size', size =(15, 1)), sg.InputText()],

            [sg.Submit(), sg.Cancel()]
        ]
        
        window = sg.Window('Qlearning App', layout)
        event, value = window.read()
        window.close()
        return value


form = Form()
value = form.FormPage()

#yapilan tekrar sayisi
iterasyon_sayisi=1000

start = value[0]
start = start.split(",")
finish = value[1]
finish = finish.split(",")
size = value[2]
size = size.split(",")




n = int(size[0])  # n burada labirentin boyutu
ekranX = n*30
ekranY = n*30
x = math.ceil(ekranX/int(n))

arkaplan = (0, 0, 0)

ekran = pygame.display.set_mode((ekranX, ekranY))
renkler = [(255, 225, 255) for i in range(n**2)]

matrix_R = np.zeros((n, n))
engel = []
engelSayisi = int(n*n*20/100)

startsPoint = []
startsPoint.append(int(start[0]))
startsPoint.append(int(start[1]))

finishPoint = []
finishPoint.append(int(finish[0]))
finishPoint.append(int(finish[1]))


#Engel atamalarini yapiyoruz
while engelSayisi != 0:
    i = r(0, n-1)
    j = r(0, n-1)
    if matrix_R[i, j] == 0 and [i, j] != [0, 0] and [i, j] != [n-1, n-1]:
        matrix_R[i, j] = -5
        engelSayisi -= 1
        renkler[n*i+j] = (255, 0, 0)
        engel.append(n*i+j)


matrix_R[int(finish[0]),int(finish[1])] = 5  # bitis noktasi
renkler[n*int(finish[0])+int(finish[1])] = (0, 255, 0)
renkler[n*int(start[0])+int(start[1])] = (0, 137, 255)
engel.append(n*(int(finish[0])) + int(finish[1]))


Q = np.zeros((n**2, 4))  
hareketler = {"yukari": 0, "asagi": 1, "sol": 2, "sag": 3}  # olasi hareket tanimlamasi
durumlar = {}
k = 0
for i in range(n):
    for j in range(n):
        durumlar[(i, j)] = k
        k += 1
alpha = 0.01
gamma = 0.9

#baslangic pozisyonu
bulunan_nokta = [int(start[0]), int(start[1])]

epsilon = 0.25


def durum_sec(bulunan_durum):
    global bulunan_nokta, epsilon
    olasi_hareket = []
    if np.random.uniform() <= epsilon:
        if bulunan_nokta[0] != 0:
            olasi_hareket.append("yukari")
        if bulunan_nokta[0] != n-1:
            olasi_hareket.append("asagi")
        if bulunan_nokta[1] != 0:
            olasi_hareket.append("sol")
        if bulunan_nokta[1] != n-1:
            olasi_hareket.append("sag")
        hareket = hareketler[olasi_hareket[r(0, len(olasi_hareket) - 1)]]
    else:
        m = np.min(Q[bulunan_durum])
        if bulunan_nokta[0] != 0:  # yukari
            olasi_hareket.append(Q[bulunan_durum, 0])
        else:
            olasi_hareket.append(m - x)
        if bulunan_nokta[0] != n-1:  # asagi
            olasi_hareket.append(Q[bulunan_durum, 1])
        else:
            olasi_hareket.append(m - x)
        if bulunan_nokta[1] != 0:  # sol
            olasi_hareket.append(Q[bulunan_durum, 2])
        else:
            olasi_hareket.append(m - x)
        if bulunan_nokta[1] != n-1:  # sag
            olasi_hareket.append(Q[bulunan_durum, 3])
        else:
            olasi_hareket.append(m - x)
        hareket = random.choice([i for i, a in enumerate(olasi_hareket) if a == max(
            olasi_hareket)]) 
    return hareket


#her turdaki tur sayisi
def tur(iterasyon, startPoint, adim, kazanc, turAdim, turKazanc,yol,olasiYollar):
    global bulunan_nokta, epsilon
    bulunan_durum = durumlar[(bulunan_nokta[0], bulunan_nokta[1])]
    hareket = durum_sec(bulunan_durum)
    if hareket == 0:  # move yukari
        bulunan_nokta[0] -= 1
    elif hareket == 1:  # move asagi
        bulunan_nokta[0] += 1
    elif hareket == 2:  # move sol
        bulunan_nokta[1] -= 1
    elif hareket == 3:  # move sag
        bulunan_nokta[1] += 1
    yeni_durum = durumlar[(bulunan_nokta[0], bulunan_nokta[1])]
    if yeni_durum not in engel:
        Q[bulunan_durum, hareket] += alpha*(matrix_R[bulunan_nokta[0], bulunan_nokta[1]] + gamma*(
            np.max(Q[yeni_durum])) - Q[bulunan_durum, hareket])
        adim += 1
        kazanc = kazanc+3
        yol.append([bulunan_nokta[0], bulunan_nokta[1]])
    else:
        Q[bulunan_durum, hareket] += alpha * \
            (matrix_R[bulunan_nokta[0], bulunan_nokta[1]] - Q[bulunan_durum, hareket])
        adim+=1
        kazanc = kazanc+matrix_R[bulunan_nokta[0], bulunan_nokta[1]]
        yol.append([bulunan_nokta[0], bulunan_nokta[1]])

        print(iterasyon, ". iterasyon")
        iterasyon += 1
        

        turAdim.append(adim)
        turKazanc.append(kazanc)
        olasiYollar.clear()
        olasiYollar=yol[:]

      
        yol.clear()
        kazanc = 0
        adim = 0
        bulunan_nokta[0] = int(start[0])
        bulunan_nokta[1] = int(start[1])

        if epsilon > 0.05:
            epsilon -= 3e-4  

    return iterasyon, adim, kazanc, turKazanc, turAdim,yol, olasiYollar


def layout(bittMi, olasıYol):
    c = 0
    if bittMi == False:
        for i in range(0, ekranX, 30):
            for j in range(0, ekranY, 30):
                pygame.draw.rect(ekran, (0, 0, 0),
                                (j, i, j+30, i+30), 0)
                pygame.draw.rect(
                    ekran, renkler[c], (j+1, i+1, j+28, i+28), 0)
                c += 1
                pygame.draw.circle(ekran, (0, 0, 0), (
                    bulunan_nokta[1]*30 + 14, bulunan_nokta[0]*30 + 14), 10, 0)
    else:
        for k in range(0,len(olasıYol)-1):
            pygame.draw.circle(ekran, (0, 0, 0), (
                    olasıYol[k][1]*30 + 14, olasıYol[k][0]*30 + 14), 10, 0)
            pygame.display.flip()

def grafikCizdir(adimlar, kazanc):
        
        f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        
        ax1.plot(np.arange(len(adimlar)), adimlar, 'g')
        ax1.set_xlabel('Tur')
        ax1.set_ylabel('Adım')
        ax1.set_title('Her Tur için Adım')

        
        ax2.plot(np.arange(len(kazanc)), kazanc, 'b')
        ax2.set_xlabel('Tur')
        ax2.set_ylabel('Kazanç')
        ax2.set_title('Her Tur için Kazanç')

        plt.tight_layout()  

        
        plt.show()


def  ciktiVer() :
    dosya = open('./engel.txt', 'w')
    dosya.write("S= start point\n")
    dosya.write("F= finish point\n")
    dosya.write("R= road\n")
    dosya.write("B= block\n")
    dosya.write("\n\n\n")
    for i in range(n) :
        for j in range(n):
            if i==startsPoint[0] and j==startsPoint[1]:
                dosya.write("({},{},S)".format(i,j))
            elif i==finishPoint[0] and j==finishPoint[1]:
                dosya.write("({},{},F)".format(i,j))
            elif(matrix_R[i][j]==0):
                dosya.write("({},{},R)".format(i,j))
            elif(matrix_R[i][j]==-5):
                dosya.write("({},{},B)".format(i,j))
        dosya.write("\n")
    dosya.close()


ciktiVer()
run = True
iterasyon = 0
adim = 0
turAdim = []
kazanc = 0
turKazanc = []
yol=[]
olasiYollar=[]


while iterasyon<=iterasyon_sayisi:
    #sleep(0.2)
    ekran.fill(arkaplan)
    layout(False, olasiYollar)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
    iterasyon, adim, kazanc,turKazanc,turAdim,yol,olasiYollar = tur(
        iterasyon, startsPoint, adim, kazanc, turAdim, turKazanc,yol,olasiYollar)


print(olasiYollar)
layout(True, olasiYollar)
grafikCizdir(turAdim,turKazanc)


pygame.quit()
