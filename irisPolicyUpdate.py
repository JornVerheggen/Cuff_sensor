import numpy as np
from naoController import naoController
from policy import Policy
import time as t
import math as m
from multiprocessing import Process, Queue
from solver import Solver
from dataIO import dataIO
from tqdm import trange
import statistics

def getRotMat(axis,rad):

    if axis == 'x':
        return np.array([[1.,0.,0.,0],
                        [0.,np.cos(rad),-np.sin(rad),0],
                        [0.,np.sin(rad),np.cos(rad),0],
                        [0,0,0,1]])
    elif axis == 'y':
        return np.array([[np.cos(rad),0,np.sin(rad),0],
                        [0,1,0,0],
                        [-np.sin(rad),0,np.cos(rad),0],
                        [0,0,0,1]])
    elif axis == 'z':
        return np.array([[np.cos(rad), -np.sin(rad), 0,0],
                        [np.sin(rad),   np.cos(rad), 0,0],
                        [0., 0., 1.,0],
                        [0,0,0,1]])

def updateTransform(original,dataIO,naoController,solver,averageX,averageY,averageZ):
        side,time,s1Input,s2Input,s3Input = dataIO.getFormattedData()
        sensT = solver.solve(s1Input,s2Input,s3Input,normalize= True)
        #transform from mm to m and reduce by mean to center sensor
        sensT[0,3] = (sensT[0,3]  - averageX) /500
        sensT[1,3] = (sensT[1,3]  - averageY) /500
        sensT[2,3] = (sensT[2,3]  - averageZ) /500


        #Get transformation of left arm with respect to torso frame
        torso2Hand = original

        # remove the left hand rotation from the transformation to get the arm transform
        wristYaw =  naoController.getlHandRotation()
        torso2Arm = np.matmul(torso2Hand,getRotMat('x',-wristYaw))

        torso2Sens = np.matmul(torso2Arm,np.matmul(getRotMat('y',-np.pi/2),getRotMat('z',np.pi/2)))

        # newT = np.matmul(RotMat('z', wristYaw),sensT)        
        newT =  np.matmul(torso2Sens,sensT)
        # print(sens2torsoRm)
        # print(newT)
        return newT


def batchHandler(queue):
    from naoController import naoController
    naoController = naoController()
    naoController.setup()

    while True:
        if not queue.empty():
            path,times = queue.get()
        naoController.playInterval(path,times)
        

if __name__ == "__main__":
    #Getting sensor information and setting up nao
    UDP_PORT = 56200
    dataIO = dataIO(UDP_PORT) #create dataIO object
    dataIO.startProcess() #start data reading tread

    solver = Solver() #Create solver object


    print("Getting average sensor value, don't move the sensor.")
    averageX = []
    averageY = []
    averageZ = []
    for i in trange(50):
        t.sleep(.1)
        _,_,s1Input,s2Input,s3Input = dataIO.getFormattedData()
        sensT = solver.solve(s1Input,s2Input,s3Input,normalize= True)
        averageX.append(float(sensT[0,3] ))
        averageY.append(float(sensT[1,3] ))
        averageZ.append(float(sensT[2,3] ))
    averageX = statistics.mean(averageX)
    averageY = statistics.mean(averageY)
    averageZ = statistics.mean(averageZ)
    print("Average X: "+str(averageX)+" average Y: "+str(averageY)+ " average Z: "+str(averageZ))


    naoController = naoController() #Create naoController object
    #move robot arm to front to start moving
    naoController.setup()

    numberOfIterations = 10
    batchSize = 5
    timePerStep = 0.05
    policy = Policy()
    policy.loadPath('whisky')

    queue = Queue()

    #sampleTime 0.1, batchSize 5
    times = [timePerStep]
    for i in range(batchSize-1):
        times.append(times[-1]+timePerStep)

    p = Process(target=batchHandler,args=([queue]))
    p.start()

    for iteration in range(numberOfIterations):
        for i in range(0,len(policy.path),batchSize):
            startBatch = i
            endBatch = i + batchSize
            print("Iteration: "+str(iteration)+" Batch: "+str(startBatch) + ' t/m ' + str(endBatch) +' out of total: '+ str(len(policy.path)))

            path = policy.path[startBatch:endBatch]
            path = [list(x.reshape((16,))) for x in path]
            for i in range(len(path)):
                for j in range(len(path[i])):
                    path[i][j] = float(path[i][j])

            newBatch = (path,times)
            queue.put(newBatch)
            isUpdated = False
            while not queue.empty():
                if not isUpdated:
                    for j in range(startBatch,endBatch):
                        policy.path[j] = updateTransform(policy.path[j],dataIO,naoController,solver,averageX,averageY,averageZ)
                    isUpdated = True
                        



