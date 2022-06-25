from re import S
from turtle import ycor
import numpy as np
from naoController import naoController
import time as t
from tqdm import trange
import pickle

class Policy:
    def __init__(self,sampleRate=20,enableNaoController = True):
        self.path = None
        if enableNaoController:
            self.naoContorller = naoController()
        self.sampleRate = float(sampleRate)
        self.sampleTime = 1 / self.sampleRate

    def loadPath(self,name):
        fp = open("savedPolicy/"+name+".pkl","rb")
        self.path = pickle.load(fp)
        fp.close()
        print("Policy loaded")

    def savePath(self,name):
        fp = open("savedPolicy/"+name+".pkl","wb")
        pickle.dump(self.path, fp)
        fp.close()
        print('Policy saved')

    def playPathSmooth(self,iterations):
        self.naoContorller.setup(startingPosition=self.path[0])
        for i in range(iterations):
            print("playing path iteration: "+ str(i))
            self.naoContorller.playPath(self.path,self.sampleTime)
    
    def playInterval(self,start,steps):
        self.naoContorller.playPath(self.path[start:start+steps],self.sampleTime)
    
    def playSingle(self,index):
        self.naoContorller.moveTo(self.path[index],interval=0.05)
    
    def recordPath(self,totalTime):
        totalTime = float(totalTime)
        self.naoContorller.setup(stiff=False)
        self.path = []

        print('Get ready to record..')
        t.sleep(.2)
        print('3.')
        t.sleep(1)
        print('2.')
        t.sleep(1)
        print('1.')
        t.sleep(1)
        print('Go!')

        for i in trange(int(totalTime/self.sampleTime)):
            t.sleep(self.sampleTime)
            lHandT = self.naoContorller.getOrientation('LArm')
            self.path.append(lHandT)
    
    def updatePath(self,update, t):
        self.path[t] = np.matmul(self.path[t],update)

class circlePolicy(Policy):

    def __init__(self,center, width, height,depth,speed):
        Policy.__init__(self,enableNaoController=False)
        self.center = center
        self.width = width
        self.height = height
        self.depth = depth
        self.speed = speed

    def createPath(self):
        circumference = 2*np.pi * np.sqrt(((self.height**2) + (self.width**2))/2)
        totalTime = circumference/self.speed
        amountOfPoints = int(totalTime * self.sampleRate)
        radiansPerPoint = (2*np.pi)/amountOfPoints

        self.path = []

        for i in range(amountOfPoints):
            rad = i * radiansPerPoint
            xCord = self.depth + self.center[0]
            yCord = ((self.width/2) * np.cos(rad)) + self.center[1]
            zCord = ((self.height/2) * np.sin(rad)) + self.center[2]
            
            homTrans = np.identity(4)
            homTrans[0,3] = homTrans[0,3] = xCord
            homTrans[1,3] = homTrans[1,3] = yCord
            homTrans[2,3] = homTrans[2,3] = zCord

            self.path.append(homTrans)
    
    def updatePath(self,xyz,q):
        if q == 1:
            self.depth += xyz[0] 
            self.width += xyz[1]
            self.height += xyz[2]
        if q == 2:
            self.depth += xyz[0] 
            self.width -= xyz[1]
            self.height += xyz[2]
        if q == 3:
            self.depth += xyz[0] 
            self.width -= xyz[1]
            self.height -= xyz[2]
        if q == 4:
            self.depth += xyz[0] 
            self.width += xyz[1]
            self.height -= xyz[2]
        self.createPath()