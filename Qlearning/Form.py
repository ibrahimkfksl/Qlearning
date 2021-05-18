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


start = value[0]
start = start.split(",")
finish = value[1]
finish = finish.split(",")
size = value[2]
size = size.split(",")











# Qlearning #
n = int(size[0])  # represents no. of side squares(n*n total squares)
scrx = 700
scry = 700
x = math.ceil(scrx/int(n))

background = (51, 51, 51)  # used to clear screen while rendering
# creating a screen using Pygame

screen = pygame.display.set_mode((scrx, scry))
colors = [(51, 51, 51) for i in range(n**2)]

#create reward matrix
reward = np.zeros((n, n))
terminals = []
penalities = int(n*n*30/100)

startsPoint = []
startsPoint.append(int(start[0]))
startsPoint.append(int(start[1]))

finishPoint = []
finishPoint.append(int(finish[0]))
finishPoint.append(int(finish[1]))


while penalities != 0:
    i = r(0, n-1)
    j = r(0, n-1)
    if reward[i, j] == 0 and [i, j] != [int(start[0]), int(start[1])] and [i, j] != [int(finish[0]), int(finish[1])]:
        reward[i, j] = -5
        penalities -= 1
        colors[n*i+j] = (255, 0, 0)
        terminals.append(n*i+j)


reward[int(finish[0]),int(finish[1])] = 5  # finish position
colors[n*int(finish[0])+int(finish[1])] = (0, 255, 0)
colors[n*int(start[0])+int(start[1])] = (0, 0, 255)
terminals.append(n**2 - 1)
print(reward)


Q = np.zeros((n**2, 4))  # Initializing Q-Table
actions = {"up": 0, "down": 1, "left": 2, "right": 3}  # possible actions
states = {}
k = 0
for i in range(n):
    for j in range(n):
        states[(i, j)] = k
        k += 1
alpha = 0.01
gamma = 0.9

#start position
current_pos = [int(start[0]), int(start[1])]

epsilon = 0.25


def select_action(current_state):
    global current_pos, epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        if current_pos[0] != 0:
            possible_actions.append("up")
        if current_pos[0] != n-1:
            possible_actions.append("down")
        if current_pos[1] != 0:
            possible_actions.append("left")
        if current_pos[1] != n-1:
            possible_actions.append("right")
        action = actions[possible_actions[r(0, len(possible_actions) - 1)]]
    else:
        m = np.min(Q[current_state])
        if current_pos[0] != 0:  # up
            possible_actions.append(Q[current_state, 0])
        else:
            possible_actions.append(m - 100)
        if current_pos[0] != n-1:  # down
            possible_actions.append(Q[current_state, 1])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != 0:  # left
            possible_actions.append(Q[current_state, 2])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != n-1:  # right
            possible_actions.append(Q[current_state, 3])
        else:
            possible_actions.append(m - 100)
        action = random.choice([i for i, a in enumerate(possible_actions) if a == max(
            possible_actions)])  # randomly selecting one of all possible actions with maximin value
    return action


def episode(iterasyon, startPoint, step, cost, epsiodeStep, epsiodeCost,road,proabilityRoad):
    global current_pos, epsilon
    current_state = states[(current_pos[0], current_pos[1])]
    action = select_action(current_state)
    if action == 0:  # move up
        current_pos[0] -= 1
    elif action == 1:  # move down
        current_pos[0] += 1
    elif action == 2:  # move left
        current_pos[1] -= 1
    elif action == 3:  # move right
        current_pos[1] += 1
    new_state = states[(current_pos[0], current_pos[1])]
    if new_state not in terminals:
        Q[current_state, action] += alpha*(reward[current_pos[0], current_pos[1]] + gamma*(
            np.max(Q[new_state])) - Q[current_state, action])
        step += 1
        cost = cost+3
        road.append([current_pos[0], current_pos[1]])
    else:
        Q[current_state, action] += alpha * \
            (reward[current_pos[0], current_pos[1]] - Q[current_state, action])
        step+=1
        cost = cost+reward[current_pos[0], current_pos[1]]
        road.append([current_pos[0], current_pos[1]])

        print(iterasyon, ". iterasyon")
        iterasyon += 1
        # print(current_pos)
        # step=round(startsPoint[0]-current_pos[0])+round(startsPoint[1]-current_pos[1])
        #print("step: ", step)
        #print("cost: ", cost)

        epsiodeStep.append(step)
        epsiodeCost.append(cost)
        proabilityRoad.clear()
        #if reward[road[len(road)-1][0],road[len(road)-1][1]]==5:
        proabilityRoad=road[:]


        #print(road)
        road.clear()
        cost = 0
        step = 0
        current_pos[0] = startPoint[0]
        current_pos[1] = startPoint[1]

        if epsilon > 0.05:
            epsilon -= 3e-4  # reducing as time increases to satisfy Exploration & Exploitation Tradeoff

    return iterasyon, step, cost, epsiodeCost, epsiodeStep,road, proabilityRoad


def layout(isFinish, probabilityRoad):
    c = 0
    if isFinish == False:
        for i in range(0, scrx, x):
            for j in range(0, scry, x):
                pygame.draw.rect(screen, (255, 255, 255),
                                (j, i, j+x, i+x), 0)
                pygame.draw.rect(
                    screen, colors[c], (j+1, i+1, j+x-1, i+x-1), 0)
                c += 1
                pygame.draw.circle(screen, (25, 129, 230), (
                    current_pos[1]*x + x/2, current_pos[0]*x + x/2), x*30/100, 0)
    else:
        for k in range(0,len(probabilityRoad)-1):
            pygame.draw.circle(screen, (25, 129, 230), (
                    probabilityRoad[k][1]*x + x/2, probabilityRoad[k][0]*x + x/2), x*30/100, 0)
            pygame.display.flip()

def plot_results(steps, cost):
        #
        f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        #
        ax1.plot(np.arange(len(steps)), steps, 'b')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Steps')
        ax1.set_title('Episode via steps')

        #
        ax2.plot(np.arange(len(cost)), cost, 'r')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Cost')
        ax2.set_title('Episode via cost')

        plt.tight_layout()  # Function to make distance between figures

        #
        plt.figure()
        plt.plot(np.arange(len(steps)), steps, 'b')
        plt.title('Episode via steps')
        plt.xlabel('Episode')
        plt.ylabel('Steps')

        #
        plt.figure()
        plt.plot(np.arange(len(cost)), cost, 'r')
        plt.title('Episode via cost')
        plt.xlabel('Episode')
        plt.ylabel('Cost')

        # Showing the plots
        plt.show()


def  ciktiVer() :
    dosya = open('engel.txt', 'w')
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
            elif(reward[i][j]==0):
                dosya.write("({},{},R)".format(i,j))
            elif(reward[i][j]==-5):
                dosya.write("({},{},B)".format(i,j))
        dosya.write("\n")
    dosya.close()


ciktiVer()
run = True
iterasyon = 0
step = 0
epsiodeStep = []
cost = 0
epsiodeCost = []
road=[]
proabilityRoad=[]


while iterasyon<=100:
    screen.fill(background)
    layout(False, proabilityRoad)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
    iterasyon, step, cost,epsiodeCost,epsiodeStep,road,proabilityRoad = episode(
        iterasyon, startsPoint, step, cost, epsiodeStep, epsiodeCost,road,proabilityRoad)


print(proabilityRoad)
layout(True, proabilityRoad)
plot_results(epsiodeStep,epsiodeCost)


pygame.quit()

