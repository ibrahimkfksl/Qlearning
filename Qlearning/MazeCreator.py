from PySimpleGUI.PySimpleGUI import ThisRow
import numpy as np
import random
import time

class Maze:
    def __init__(self, maze_size,start,finish):
        self.maze_size=int(maze_size)
        self.maze=np.zeros((maze_size,maze_size),dtype=float)
        self.matrix_R=np.zeros((maze_size*maze_size,maze_size*maze_size),dtype=int)
        self.matrix_Q=np.zeros((maze_size*maze_size,maze_size*maze_size),dtype=int)
        self.gamma=0.9
        self.iteration=1000


        start1 = start.split(",") #matrix size as array
        finish1=finish.split(",")

        startRow=int(start1[0])
        startColumn=int(start1[1])
        finishRow=int(finish1[0])
        finishColumn=int(finish1[1])
        self.startState=startRow*maze_size+startColumn
        self.finishState=finishRow*maze_size+finishColumn
        

        for i in range(self.maze_size):
            randomArray=self.randomIndex()
            for j in range(0,len(randomArray)):
                self.maze[i][randomArray[j]]=-1

        # Buradaki döngü kalkacak
        ###for i in range(self.maze_size):
        ###    randomArray=self.randomIndex()
        ###    for j in range(self.maze_size):
        ###        self.maze[i][j]=0

        #Matris_R i olusturuyoruz
        for i in range(self.maze_size*self.maze_size):   
          for j in range(self.maze_size*self.maze_size):
            self.matrix_R[i][j]=-1
        self.createRMatrix()
        self.addFinishState(self.finishState)
        self.printMatrix_R()
        self.run()
        self.printMatrix_Q()
        #self.testCiktiVer()
        
    def randomIndex(self):
        block_sum=int((self.maze_size*30)/100)
        randomArray=[]
        for i in range(0,block_sum):
            flag=False
            r=random.randint(0,self.maze_size-1)
            for j in range(0,len(randomArray)):
                if randomArray[j]==r:
                    flag=True
                    break
            
            if flag==True:
                i=i-2
                continue
            else:
                randomArray.append(r)
        
        return randomArray

    
    def printMaze(self):
        print(self.maze)
    
    def printMatrix_R(self):
        print(self.matrix_R)

    def printMatrix_Q(self):
        print(self.matrix_Q)
    
    def editMaze(self,row,column,value):
        self.maze[row][column]=value
    
    def createRMatrix(self):
        state_number=int
        for i in range(self.maze_size):   
          for j in range(self.maze_size):
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

        #self.matrix_R[state_number][state_number]=100
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
            self.matrix_R[state_number][oldRow*self.maze_size+oldColumn]=100

    def getMaze(self):
        return self.maze
    def getMatrixR(self):
        return self.matrix_R
    def getFinishState(self):
        return self.finishState
    
        
    def run(self):
        iteration=300000
        probabilityState=[]
        matrisSize=self.maze_size*self.maze_size
        #r=random.randint(0, matrisSize-1)
        r=self.startState
        for i in range(0,iteration):
            b=0

            for j in range(matrisSize):
                if(self.matrix_R[r][j]!=-1):
                    probabilityState.append(j)

            if  probabilityState:
                
            randomIndex=random.randint(0,len(probabilityState)-1)
            avabilityState=probabilityState[randomIndex]
            probabilityState.clear()

            flag=0
            for j in range(0,matrisSize):
                probabilityState.append(self.matrix_Q[avabilityState][j])
                flag=flag+self.matrix_Q[avabilityState][j]
            
            if flag==0:
                b=0
                probabilityState.clear()
            else:
                for j in range(0,len(probabilityState)):
                    if(probabilityState[j]>=0):
                        b=probabilityState[j]
                probabilityState.clear()

            self.matrix_Q[r][avabilityState]=int(self.matrix_R[r][avabilityState]+(self.gamma*b))

            if(self.matrix_R[r][avabilityState]==100):
                r=random.randint(0, matrisSize-1)
            else:
                r=avabilityState

            

    def testCiktiVer(self):
        enb=0
        for i in range(self.maze_size*self.maze_size):
            for j in range(self.maze_size*self.maze_size):
                if self.matrix_Q[i][j]>enb:
                    enb=self.matrix_Q[i][j]
        

        flag=0
        index=self.startState
        indexFlag=self.startState
        print("index: ",index," value: ", flag )
        while(flag<enb):
            for i in range(self.maze_size*self.maze_size):
                if self.matrix_Q[index][i]>flag:
                    flag=self.matrix_Q[index][i]
                    indexFlag=i
            
            index=indexFlag
            print("index: ",index," value: ", flag )








        






    
