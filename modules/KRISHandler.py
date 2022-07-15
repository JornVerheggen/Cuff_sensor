import numpy as np 
import sys
import time as t
import math as m
from solver import Solver
from naoController import NaoController
from dataIO import DataIO
from rotMat import getEuler3, getRotmat3, getRotmat4, getRotMatFromEuler, mm, getEuler4

class KRISHandler():

    def __init__(self):
        self.collectionCounter = 0
        self.xyz = [0,0,0]
        self.rxyz = [0,0,0]

        UDP_PORT = 56200   
        self.dataIO = DataIO(UDP_PORT) #create dataIO object
        self.dataIO.startProcess() #start data reading tread

        self.solver = Solver() #Create solver object

        self.nc = NaoController() #Create naoController object

        #Create offset
        _,_,s1Input,s2Input,s3Input = self.dataIO.getFormattedData()
        self.offsetT = self.solver.solve(s1Input,s2Input,s3Input,normalize= False)
        self.offsetTRot = np.linalg.inv(self.offsetT[:3,:3])
        self.offsetTTrans = self.offsetT[:3,3] * -1

    def getThresholdedValue(self,x,thresholdVal):
        if x > 0:
            if x > thresholdVal:
                x -= thresholdVal
            else:
                x = 0
        elif x < 0:
            if x < -thresholdVal:
                x += thresholdVal
            else:
                x = 0
        return x
        
    def softClip(self,x,clipVal):
        return clipVal*np.tanh(x/clipVal)

    def getHand2SensHom(self,handYaw):
        result = np.identity(4)
        result[:3,:3] = getRotmat3('x',handYaw) #handYaw has to be positive

        #values for 0.05775 and 0.01231 obtained from nao documentation
        #value for 0.015 estimation of sensor position on arm
        trans =  np.array([0.05775+0.015,0,0.01231])
        result[:3,3] = trans
        return result

    def getSingleTransform(self):
        #Get transformation of left arm with respect to torso frame
        torso2Hand = self.nc.getOrientation('LArm')
        torso2HandRot = torso2Hand[:3,:3]
        torso2HandTrans = torso2Hand[:,3]
        wristYaw = self.nc.getlHandRotation()

        #Get data from sensor
        _,_,s1Input,s2Input,s3Input = self.dataIO.getFormattedData()
        sensT = self.solver.solve(s1Input,s2Input,s3Input,normalize= False)

        sensTRot = sensT[:3,:3]
        sensTTrans = sensT[:3,3]

        newSensTTrans = sensTTrans + self.offsetTTrans
        newSensTTrans[0] = self.getThresholdedValue(sensTTrans[0],0.003)*-5
        newSensTTrans[1] = 0.
        newSensTTrans[2] = 0.

        #GET the rotation
        newSensTRot = mm(sensTRot,self.offsetTRot)
        sensXr,sensYr,sensZr = getEuler3(sensTRot)

        sensXr = self.softClip(self.getThresholdedValue(sensXr,0.018),np.pi/3)/3
        sensYr = self.softClip(self.getThresholdedValue(sensYr,0.018),np.pi/3)/3
        sensZr = self.softClip(self.getThresholdedValue(sensZr,0.018),np.pi/3)/3

        newSensTRot = getRotMatFromEuler(np.array([0,sensYr,sensZr]))

        #Create new homogeneous sensor transform
        newSensT = np.identity(4)
        newSensT[:3,:3] = newSensTRot
        newSensT[:3,3] = newSensTTrans

        #Find new position for the hand
        a = mm(torso2Hand,np.linalg.inv(self.getHand2SensHom(wristYaw)))
        b = mm(a,np.linalg.inv(newSensT))
        c = mm(b,self.getHand2SensHom(wristYaw))

        return c

    def gatherInput(self):
        newValue = self.getSingleTransform()
        currentPosition = self.nc.getOrientation('LArm')

        relativeAdjustment = mm(np.linalg.inv(currentPosition),newValue)
        relativeEuler = getEuler4(relativeAdjustment)

        self.collectionCounter += 1 
        self.xyz[0] += relativeEuler[0]
        self.xyz[1] += relativeEuler[1]
        self.xyz[2] += relativeEuler[2]

        self.rxyz[0] += relativeEuler[3]
        self.rxyz[1] += relativeEuler[4]
        self.rxyz[2] += relativeEuler[5]
        

    def collectInput(self):

        if self.collectionCounter > 0:
            xyz  = []
            rxyz = []
            for i in self.xyz:
                xyz.append((float(i)/self.collectionCounter))
            for i in self.rxyz:
                rxyz.append((float(i)/self.collectionCounter))
        else:
            xyz = [0,0,0]
            rxyz = [0,0,0]

        self.collectionCounter = 0
        self.xyz = [0,0,0]
        self.rxyz = [0,0,0]

        return (np.array(xyz),np.array(rxyz))