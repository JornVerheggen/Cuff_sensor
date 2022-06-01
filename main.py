from re import L
import numpy as np 
import sys
from solver import Solver
from naoController import naoController
import time
import math
from scipy.spatial.transform import Rotation as R

def RotMat(axis,rad):

    if axis == 'x':
        return np.array([[1.,0.,0.],
                        [0.,np.cos(rad),-np.sin(rad)],
                        [0.,np.sin(rad),np.cos(rad)]])
    elif axis == 'y':
        return np.array([[np.cos(rad),0,np.sin(rad)],
                        [0,1,0],
                        [-np.sin(rad),0,np.cos(rad)]])
    elif axis == 'z':
        return np.array([[np.cos(rad), -np.sin(rad), 0],
                        [np.sin(rad),   np.cos(rad), 0],
                        [0., 0., 1.]])


solver = Solver() #Create solver object
naoController = naoController() #Create naoController object


#move robot arm to front to start moving
naoController.setup()


while True:
    #Get data from sensor
    side,time,s1Input,s2Input,s3Input = getData(UDP_PORT)
    sensTrans, sensRot = solver.solve(s1Input,s2Input,s3Input,normalize= True)
    sensTrans /=1000

    # #Get transformation of left arm with respect to torso frame
    lHandT = naoController.getOrientation('LArm')
    lHandT = np.array(lHandT.toVector()).reshape(4,4)
    lHandR = lHandT[:3].T[:3].T
    wristYaw =  naoController.getlHandRotation()
    lArmR = np.matmul(RotMat('x',-wristYaw),lHandR)

    sens2torsoRm = np.matmul(np.matmul(lArmR,RotMat('y',-np.pi/2)),RotMat('z',np.pi/2))
    
    newPos =  np.matmul(sens2torsoRm,sensTrans)

    naoController.relativeMove(newPos)
