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

    #Create offset
    _,_,s1Input,s2Input,s3Input = dataIO.getFormattedData()
    solver.setOffset(s1Input,s2Input,s3Input)

    while True:
        #Get data from sensor
        side,time,s1Input,s2Input,s3Input = dataIO.getFormattedData()
        print(time)
        sensT = solver.solve(s1Input,s2Input,s3Input,normalize= False)

        #Get transformation of left arm with respect to torso frame
        torso2Hand = naoController.getOrientation('LArm')

        # remove the left hand rotation from the transformation to get the arm transform
        wristYaw =  naoController.getlHandRotation()
        torso2Arm = np.matmul(torso2Hand,RotMat('x',-wristYaw))

        torso2Sens = np.matmul(torso2Arm,np.matmul(RotMat('y',-np.pi/2),RotMat('z',np.pi/2)))

        # newT = np.matmul(RotMat('z', wristYaw),sensT)        
        newT =  np.matmul(torso2Sens,sensT)
        # print(sens2torsoRm)
        # print(newT)
        naoController.moveTo(newT)
