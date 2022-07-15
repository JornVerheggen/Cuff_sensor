from modules.KRISHandler import KRISHandler
from modules.keyBoardHandler import KeyboardHandler
from modules.naoController import NaoController
from modules.rotMat import getEuler4
from multiprocessing import Process, Queue
import numpy as np
import pickle
import time as t
import math as m

def batchHandler(queue,startPos):
    from modules.naoController import NaoController
    nc = NaoController()
    nc.setup(startingPosition=startPos)
    nc.say("start")
    while True:
        if not queue.empty():
            path,times = queue.get()
            nc.playInterval(path,times)

class CircleStopTest:
    def __init__(self,method,participant):
        #SETTINGS   
        self.participant = participant
        self.method = method
        self.batchSize = 10
        self.intervalTime = 0.02
        self.minIntervalTime = 0.01
        self.stopIntervalTime = 0.05

        #Create path
        self.createPath()
        self.points = len(self.path)

        #Set up modules
        self.nc = NaoController()
        if self.method == 'keyboard':
            self.kbh = KeyboardHandler()
        if self.method == 'KRIS':
            self.krisHandler = KRISHandler()

    def gatherKeyboardInput(self,tEnd):
        while t.time() < tEnd:
            self.kbh.gatherInput()
        return self.kbh.collectInput()

    def gatherKRISInput(self,tEnd):
        while t.time() < tEnd:
            self.krisHandler.gatherInput()
        return self.krisHandler.collectInput()
        

    def createPath(self):
        fp1 = open ("C:/Users/jorn-/Documents/school/y2/thesis/cuffling/code/Cuff_sensor/savedPolicy/stopExperiment3.pkl", "rb")
        self.path = pickle.load(fp1)        

    def updateSpeed(self,adjustment,startIndex,stopIndex):
        pointA = self.path[startIndex][:3,3]
        pointB = self.path[stopIndex][:3,3]

        direction = pointB-pointA

        if direction.any() != np.array([0.,0.,0.]).all() and adjustment.any() != np.array([0.,0.,0.]).all(): 
            directionFactor = np.arccos(np.dot(direction,adjustment)/(np.linalg.norm(direction) * np.linalg.norm(adjustment)))
            directionFactor /= np.pi
            directionFactor -= 0.5
            directionFactor *= -2
        else:
            directionFactor = 0.0
        
        # speedFactor = np.linalg.norm(adjustment)
        speedAdjustment = directionFactor *.001 #* speedFactor

        self.intervalTime -= speedAdjustment
        if self.intervalTime <= self.minIntervalTime:
            self.intervalTime = self.minIntervalTime

        print(self.intervalTime)
        return (direction,directionFactor,self.intervalTime)

    def run(self):
        #setup

        path = "C:/Users/jorn-/Documents/school/y2/thesis/cuffling/code/Cuff_sensor/data/stopExperiment/"+str(self.participant)+ '/'

        if self.method == 'KRIS':
            inputFp = open(path +'KRISInputData.csv','w+')
            outputFp = open(path +'KRISOutputData.csv','w+')

        if self.method == 'keyboard':
            inputFp = open(path +'keyboardInputData.csv','w+')
            outputFp = open(path +'keyboardOutputData.csv','w+')

        self.queue = Queue()
        startPos = self.path[0]
        p = Process(target=batchHandler,args=((self.queue,startPos)))
        p.start()
        t.sleep(10)

        for startIndex in range(0,self.points - (self.batchSize + 1),self.batchSize):
            stopIndex = startIndex + self.batchSize
            #Send command
            if startIndex > stopIndex:
                batchPath = self.path[startIndex:self.points] + self.path[0:stopIndex]
            else: 
                batchPath = self.path[startIndex:stopIndex]
            
            for i, pos in enumerate(batchPath):
                pos = list(pos.reshape((16,)))
                pos = [float(x) for x in pos]
                batchPath[i] = pos
            
            intervals = [(x * self.intervalTime) + self.intervalTime for x in range(self.batchSize)]
            while(not self.queue.empty()):
                t.sleep(.001)
            self.queue.put((batchPath,intervals))
            #Gather input
            tStart = t.time()
            tEnd = tStart + intervals[-1]

            if self.method == 'KRIS':
                transAdjustment, rotAdjustment = self.gatherKRISInput(tEnd)
            if self.method == 'keyboard':
                transAdjustment, rotAdjustment = self.gatherKeyboardInput(tEnd)
            #Update speed
            direction,directionFactor,speedAdjustment = self.updateSpeed(transAdjustment,startIndex,stopIndex)
            #Log data

            inputFp.write(
                str(transAdjustment[0]) + ';' +
                str(transAdjustment[1]) + ';' +
                str(transAdjustment[2]) + ';' +
                str(rotAdjustment[0]) + ';' + 
                str(rotAdjustment[1]) + ';' + 
                str(rotAdjustment[2]) + '\n')

            outputFp.write( str(startIndex) +  ';' +
                            str(stopIndex) +  ';' +
                            str(direction[0]) + ';' +
                            str(direction[1]) + ';' +
                            str(direction[2]) + ';' +  
                            str(directionFactor) + ';' +
                            # str(speedFactor) +  ';' +
                            str(speedAdjustment) + '\n')

            #Closing condition
            if self.intervalTime > self.stopIntervalTime:
                print("speed low enough")
                self.nc.say("Successfully stopped")
                break

        print("Experiment stopped")


if __name__ == '__main__':
    demoType = raw_input("Type of demonstration: \'keyboard\' or \'KRIS\'")
    print("Demo type is: " + demoType)

    participantNumber = int(raw_input('Participant number: '))
    cst = CircleStopTest(demoType,participantNumber)

    print("Running stop experiment with demo method: " + demoType + " and participant: " + str(participantNumber))

    cst.run()