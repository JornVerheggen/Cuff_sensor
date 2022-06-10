from re import S
import numpy as np
from naoController import naoController
import time as t
from tqdm import trange
import pickle

class Policy:
    def __init__(self,sampleRate=20):
        self.path = None
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
        self.naoContorller.setup()
        for i in range(iterations):
            print("playing path iteration: "+ str(i))
            self.naoContorller.playPath(self.path,self.sampleTime)
    
    def playInterval(self,start,steps):
        self.naoContorller.playPath(self.path[start:start+steps],self.sampleTime)
    
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

#Policy player
# if __name__ == '__main__':
#     policy = Policy()
#     policy.naoContorller.setup()
#     policy.loadPath('whisk')
#     policy.playPathSmooth(3)

#Policy recorder
if __name__ == '__main__':
    policy = Policy()
    policy.recordPath(8)
    policy.playPathSmooth(2)
    t.sleep(1)
    policy.savePath('whisky3')
    