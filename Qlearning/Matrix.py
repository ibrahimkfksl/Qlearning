import pygame 
import math

class Matrix:
    def __init__(self, X, Y, start, finish, maze):
        start = start.split(',')
        finish = finish.split(',')
        self.BLACK = (0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.GREY = (212, 194, 193)
        self.GREEN = (124,252,0)
        self.RED = (220,20,60)
        self.BLUE = (0,0,255)
        self.WINDOW_HEIGHT = 800
        self.WINDOW_WIDTH = 800
        self.X = math.ceil(800/int(X))
        self.Y = math.ceil(800/int(Y))
        self.START_X = int(start[0])*(self.X)
        self.START_Y = int(start[1])*(self.Y)
        self.FINISH_X = int(finish[0])*(self.X)
        self.FINISH_Y = int(finish[1])*(self.Y)
        self.maze = maze
        self.main()

    def main(self):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(self.BLACK)

        while True:
            self.drawGrid(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()


    def drawGrid(self , SCREEN):
        i=0
        j=0
        for x in range(0, self.WINDOW_WIDTH, (self.X)):
            for y in range(0, self.WINDOW_HEIGHT, (self.Y)):
                if(x == self.START_X and y == self.START_Y):
                    pygame.draw.rect(SCREEN, self.GREEN, pygame.Rect(x, y, (self.X)-2, (self.Y)-1))
                elif(x == self.FINISH_X and y == self.FINISH_Y):
                     pygame.draw.rect(SCREEN, self.RED, pygame.Rect(x, y, (self.X)-2, (self.Y)-1))
                elif(self.maze[j][i] == -1):
                    pygame.draw.rect(SCREEN, self.BLUE, pygame.Rect(x, y, (self.X)-2, (self.Y)-1))
                else:
                    pygame.draw.rect(SCREEN, self.GREY, pygame.Rect(x, y, (self.X)-2, (self.Y)-1))
                j+=1
            i = i+1
            j=0