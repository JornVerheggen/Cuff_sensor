import numpy as np
# from naoController import NaoController
# import time as t
# from tqdm import trange
# import pickle
import matplotlib.pyplot as plt

class Policy:
    def __init__(self,sampleRate=20,enableNaoController = True):
        self.path = None
        if enableNaoController:
            self.nc = NaoController()
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
        self.nc.setup(startingPosition=self.path[0])
        for i in range(iterations):
            print("playing path iteration: "+ str(i))
            self.nc.playPath(self.path,self.sampleTime)
    
    def playInterval(self,start,steps):
        self.nc.playPath(self.path[start:start+steps],self.sampleTime)
    
    def playSingle(self,index):
        self.nc.moveTo(self.path[index],interval=0.05)
    
    def recordPath(self,totalTime):
        totalTime = float(totalTime)
        self.nc.setup(stiff=False)
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
            lHandT = self.nc.getOrientation('LArm')
            self.path.append(lHandT)
    
    def updatePath(self,update, t):
        self.path[t] = np.matmul(self.path[t],update)

class circlePolicy(Policy):

    def __init__(self,center, width, height,depth,pitch,speed):
        Policy.__init__(self,enableNaoController=False)
        self.center = center
        self.width = width
        self.height = height
        self.depth = depth
        assert pitch != 0
        self.pitch = pitch
        self.speed = speed

    def createPath(self):
        circumference = 2*np.pi * np.sqrt(((self.height**2) + (self.width**2))/2)
        totalTime = circumference/self.speed
        amountOfPoints = int(totalTime * self.sampleRate)
        radiansPerPoint = (2*np.pi)/amountOfPoints

        self.path = []

        for i in range(amountOfPoints):
            rad = i * radiansPerPoint
            xCord = (((self.height/2) * np.sin(rad))/np.tan(self.pitch)) + self.center[0]
            yCord = ((self.width/2) * np.cos(rad)) + self.center[1]
            zCord = ((self.height/2) * np.sin(rad)) + self.center[2]
            
            homTrans = np.identity(4)
            homTrans[0,3] = homTrans[0,3] = xCord
            homTrans[1,3] = homTrans[1,3] = yCord
            homTrans[2,3] = homTrans[2,3] = zCord

            self.path.append(homTrans)
    
    def updatePath(self,xyz,q):
        x = 0.1
        if q == 1:
            self.pitch += xyz[0] * x
            self.width += xyz[1]
            self.height += xyz[2]
        if q == 2:
            self.pitch += xyz[0]  * x
            self.width -= xyz[1]
            self.height += xyz[2]
        if q == 3:
            self.pitch -= xyz[0]  * x
            self.width -= xyz[1]
            self.height -= xyz[2]
        if q == 4:
            self.pitch -= xyz[0]  * x
            self.width += xyz[1]
            self.height -= xyz[2]
        self.createPath()

class antiprism(Policy):

    def __init__(self,center, width, height,depth1,depth2,speed,points):
        #Policy.__init__(self,enableNaoController=False)
        self.center = center
        self.width = width
        self.height = height
        self.depth1 = depth1
        self.depth2 = depth2
        self.speed = speed
        self.points = points

    def createPath(self):
        self.vertecies = []
        angle = 2*np.pi / (self.points*2)
        front = False
        for p in range(self.points*2):

            y = np.cos(angle*p) * self.width/2
            z = np.sin(angle*p) * self.height/2

            if front:
                front = False
                x = self.depth1
                self.vertecies.append((x,y,z))
            else:
                front = True
                x = self.depth2
                self.vertecies.append((x,y,z))
        self.vertecies.append(self.vertecies[0])

# if __name__ == '__main__':
#     p1= antiprism((0,0,0),5,5,1,-1,0.001,4)
#     p1.createPath()
#     print(p1.vertecies)
#     x,y,z = zip(*p1.vertecies)
#     fig = plt.figure()
#     ax = plt.axes(projection="3d")
#     ax.plot3D(x,y,z)
#     plt.show()