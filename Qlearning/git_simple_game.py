import numpy as np
import pygame
from time import time, sleep
from random import randint as r
import random
import matplotlib.pyplot as plt



n = 7  # represents no. of side squares(n*n total squares)
scrx = n*100
scry = n*100
background = (51, 51, 51)  # used to clear screen while rendering
# creating a screen using Pygame
screen = pygame.display.set_mode((scrx, scry))
colors = [(51, 51, 51) for i in range(n**2)]
reward = np.zeros((n, n))
terminals = []
penalities = int(n*n*30/100)

startsPoint = []
startsPoint.append(0)
startsPoint.append(0)

finishPoint = []
finishPoint.append(n-1)
finishPoint.append(n-1)


while penalities != 0:
    i = r(0, n-1)
    j = r(0, n-1)
    if reward[i, j] == 0 and [i, j] != [0, 0] and [i, j] != [n-1, n-1]:
        reward[i, j] = -5
        penalities -= 1
        colors[n*i+j] = (255, 0, 0)
        terminals.append(n*i+j)


reward[finishPoint[0],finishPoint[0]] = 5  # finish block
colors[n**2 - 1] = (0, 255, 0)
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
current_pos = [0, 0]
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
    # print(new_state)
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
        if reward[road[len(road)-1][0],road[len(road)-1][1]]==5:
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


def layout():
    c = 0
    screenx = int(scrx/n)
    screeny = int(scry/n)
    for i in range(0, scrx, screenx):
        for j in range(0, scry, screeny):
            pygame.draw.rect(screen, (255, 255, 255),
                             (j, i, j+screeny, i+screenx), 0)
            pygame.draw.rect(
                screen, colors[c], (j+1, i+1, j+screeny-1, i+screenx-1), 0)
            c += 1
            pygame.draw.circle(screen, (25, 129, 230), (
                current_pos[1]*screenx + screenx/2, current_pos[0]*screenx + screenx/2), 30, 0)


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


while iterasyon<=1:
    # sleep(0.3)
    screen.fill(background)
    layout()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
    iterasyon, step, cost,epsiodeCost,epsiodeStep,road,proabilityRoad = episode(
        iterasyon, startsPoint, step, cost, epsiodeStep, epsiodeCost,road,proabilityRoad)
print(proabilityRoad)
plot_results(epsiodeStep,epsiodeCost)

pygame.quit()

