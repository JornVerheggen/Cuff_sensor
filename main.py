import numpy as np 
import sys
from solver import Solver
from naoController import naoController
from dataIO import dataIO
import time as t
import math

def RotMat(axis,rad):

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

if __name__ == '__main__':
    UDP_PORT = 56200
    dataIO = dataIO(UDP_PORT) #create dataIO object
    dataIO.startProcess() #start data reading tread

    solver = Solver() #Create solver object

    naoController = naoController() #Create naoController object
    #move robot arm to front to start moving
    naoController.setup()


    while True:
        #Get data from sensor
        side,time,s1Input,s2Input,s3Input = dataIO.getFormattedData()
        print(time)
        sensT = solver.solve(s1Input,s2Input,s3Input,normalize= True)

        #transform from mm to m
        sensT[0,3] = sensT[0,3] /1000
        sensT[1,3] = sensT[1,3] /1000
        sensT[2,3] = sensT[2,3] /1000

        #Get transformation of left arm with respect to torso frame
        lHandT = naoController.getOrientation('LArm')

        # remove the left hand rotation from the transformation to get the arm transform
        wristYaw =  naoController.getlHandRotation()
        lArmT = np.matmul(lHandT,RotMat('x',-wristYaw))

        sens2torsoRm = np.matmul(lArmT,np.matmul(RotMat('y',-np.pi/2),RotMat('z',np.pi/2)))

        newT = np.matmul(RotMat('z', wristYaw),sensT)        
        newT =  np.matmul(sens2torsoRm,newT)
        # print(sens2torsoRm)
        # print(newT)

        naoController.moveTo(newT)
