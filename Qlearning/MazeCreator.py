from PySimpleGUI.PySimpleGUI import ThisRow
import numpy as np
import random

class Maze:
    def __init__(self, maze_size):
        self.maze_size=int(maze_size)
        self.maze=np.zeros((maze_size,maze_size),dtype=float)
        self.matrix_R=np.zeros((maze_size*maze_size,maze_size*maze_size),dtype=int)

        #Maze e engel atamasi yapiyoruz
        for i in range(self.maze_size):   
          flag=0
          block_sum=int((maze_size*30)/100)
          for j in range(self.maze_size):
              r=random.randint(-1,0)
              if r==-1:
                  if flag<=block_sum:
                      self.maze[i][j]=-1
                      flag=flag+1
                  else:
                      self.maze[i][j]=0
              else:
                  self.maze[i][j]=0

              #Buradaki kod engelsiz bir maze olusturmak icin
              #self.maze[i][j]=0
        
        
        #Matris_R i olusturuyoruz
        for i in range(self.maze_size*self.maze_size):   
          for j in range(self.maze_size*self.maze_size):
            self.matrix_R[i][j]=-1
        
            
    def printMaze(self):
        print(self.maze)
    
    def printMatrix_R(self):
        print(self.matrix_R)
    
    def editMaze(self,row,column,value):
        self.maze[row][column]=value
    
    def createRMatrix(self):
        state_number=int
        for i in range(self.maze_size):   
          for j in range(self.maze_size):
              print(i,"-",j)
              if self.maze[i][j]==-1 and i==j:
                  continue


                #Sol Ust Kose
              if i==0 and j==0:
                self.editMatrixR(i, j, i + 1, j)
                self.editMatrixR(i, j, i, j + 1)
                self.editMatrixR(i, j, i + 1, j + 1)
            
                #sag ust kose
              elif i==0 and j==self.maze_size-1:
                   self.editMatrixR(i, j, i, j - 1)
                   self.editMatrixR(i, j, i + 1, j - 1)
                   self.editMatrixR(i, j, i + 1, j)

                #sol alt kose
              elif i==self.maze_size-1 and j==0:
                    self.editMatrixR(i, j, i - 1, j)
                    self.editMatrixR(i, j, i - 1, j + 1)
                    self.editMatrixR(i, j, i, j + 1)
              
                #sag alt kose
              elif i==self.maze_size-1 and j==self.maze_size-1:
                    self.editMatrixR(i, j, i, j - 1)
                    self.editMatrixR(i, j, i - 1, j - 1)
                    self.editMatrixR(i, j, i - 1, j)

                #ust satir
              elif i==0 and j>0 and j< self.maze_size-1:
                    self.editMatrixR(i, j, i, j - 1)
                    self.editMatrixR(i, j, i + 1, j - 1)
                    self.editMatrixR(i, j, i + 1, j)
                    self.editMatrixR(i, j, i + 1, j + 1)
                    self.editMatrixR(i, j, i, j + 1)
            
                #sol sutun
              elif i!=0 and i!=self.maze_size-1 and j==0:
                    self.editMatrixR(i, j, i - 1, j)
                    self.editMatrixR(i, j, i - 1, j + 1)
                    self.editMatrixR(i, j, i, j + 1)
                    self.editMatrixR(i, j, i + 1, j + 1)
                    self.editMatrixR(i, j, i + 1, j)
            
                #sag ustun
              elif i!=0 and i!= self.maze_size-1 and j==self.maze_size-1:
                    self.editMatrixR(i, j, i - 1, j)
                    self.editMatrixR(i, j, i - 1, j - 1)
                    self.editMatrixR(i, j, i, j - 1)
                    self.editMatrixR(i, j, i + 1, j - 1)
                    self.editMatrixR(i, j, i + 1, j)

                #alt satir
              elif i==self.maze_size-1 and j!=0 and j!=self.maze_size-1:
                    self.editMatrixR(i, j, i, j - 1)
                    self.editMatrixR(i, j, i - 1, j - 1)
                    self.editMatrixR(i, j, i - 1, j)
                    self.editMatrixR(i, j, i - 1, j + 1)
                    self.editMatrixR(i, j, i, j + 1)

                #ortada kalan degerler
              else:
                    self.editMatrixR(i, j, i, j - 1)
                    self.editMatrixR(i, j, i - 1, j - 1)
                    self.editMatrixR(i, j, i - 1, j)
                    self.editMatrixR(i, j, i - 1, j + 1)
                    self.editMatrixR(i, j, i, j + 1)
                    self.editMatrixR(i, j, i + 1, j + 1)
                    self.editMatrixR(i, j, i + 1, j)
                    self.editMatrixR(i, j, i + 1, j - 1)



    def editMatrixR(self,oldRow,oldColumn,newRow,newColumn):
        if self.maze[newRow][newColumn]==0:
            state_number=int(newRow*self.maze_size+newColumn)
            self.matrix_R[oldRow*self.maze_size+oldColumn][state_number]=0



    def addFinishState(self, state_number):
        row=int(state_number/self.maze_size)
        column=state_number-(row*self.maze_size)

        i=row
        j=column

        #Sol Ust Kose
        if i==0 and j==0:
            self.editFinishState(i, j, i + 1, j)
            self.editFinishState(i, j, i, j + 1)
            self.editFinishState(i, j, i + 1, j + 1)
            
        #sag ust kose
        elif i==0 and j==self.maze_size-1:
            self.editFinishState(i, j, i, j - 1)
            self.editFinishState(i, j, i + 1, j - 1)
            self.editFinishState(i, j, i + 1, j)

        #sol alt kose
        elif i==self.maze_size-1 and j==0:
            self.editFinishState(i, j, i - 1, j)
            self.editFinishState(i, j, i - 1, j + 1)
            self.editFinishState(i, j, i, j + 1)
              
        #sag alt kose
        elif i==self.maze_size-1 and j==self.maze_size-1:
            self.editFinishState(i, j, i, j - 1)
            self.editFinishState(i, j, i - 1, j - 1)
            self.editFinishState(i, j, i - 1, j)

        #ust satir
        elif i==0 and j>0 and j< self.maze_size-1:
            self.editFinishState(i, j, i, j - 1)
            self.editFinishState(i, j, i + 1, j - 1)
            self.editFinishState(i, j, i + 1, j)
            self.editFinishState(i, j, i + 1, j + 1)
            self.editFinishState(i, j, i, j + 1)
            
        #sol sutun
        elif i!=0 and i!=self.maze_size-1 and j==0:
            self.editFinishState(i, j, i - 1, j)
            self.editFinishState(i, j, i - 1, j + 1)
            self.editFinishState(i, j, i, j + 1)
            self.editFinishState(i, j, i + 1, j + 1)
            self.editFinishState(i, j, i + 1, j)
            
        #sag ustun
        elif i!=0 and i!= self.maze_size-1 and j==self.maze_size-1:
            self.editFinishState(i, j, i - 1, j)
            self.editFinishState(i, j, i - 1, j - 1)
            self.editFinishState(i, j, i, j - 1)
            self.editFinishState(i, j, i + 1, j - 1)
            self.editFinishState(i, j, i + 1, j)

        #alt satir
        elif i==self.maze_size-1 and j!=0 and j!=self.maze_size-1:
            self.editFinishState(i, j, i, j - 1)
            self.editFinishState(i, j, i - 1, j - 1)
            self.editFinishState(i, j, i - 1, j)
            self.editFinishState(i, j, i - 1, j + 1)
            self.editFinishState(i, j, i, j + 1)

        #ortada kalan degerler
        else:
            self.editFinishState(i, j, i, j - 1)
            self.editFinishState(i, j, i - 1, j - 1)
            self.editFinishState(i, j, i - 1, j)
            self.editFinishState(i, j, i - 1, j + 1)
            self.editFinishState(i, j, i, j + 1)
            self.editFinishState(i, j, i + 1, j + 1)
            self.editFinishState(i, j, i + 1, j)
            self.editFinishState(i, j, i + 1, j - 1)


    def editFinishState(self,oldRow,oldColumn,newRow,newColumn):
        if self.maze[newRow][newColumn]==0:
            state_number=int(newRow*self.maze_size+newColumn)
            self.matrix_R[oldRow*self.maze_size+oldColumn][state_number]=100

    def getMaze(self):
        return self.maze
    def getMatrixR(self):
        return self.matrix_R
