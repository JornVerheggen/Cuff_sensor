import numpy as np 
import sys
import time as t
import math as m
from modules.solver import Solver
from modules.naoController import NaoController
from modules.dataIO import DataIO
from modules.rotMat import getEuler3, getRotmat3, getRotmat4, getRotMatFromEuler, mm

def getThresholdedValue(x,thresholdVal):
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
    
def softClip(x,clipVal):
    return clipVal*np.tanh(x/clipVal)


def getHand2SensHom(handYaw):
    result = np.identity(4)
    result[:3,:3] = getRotmat3('x',handYaw) #handYaw has to be positive

    #values for 0.05775 and 0.01231 obtained from nao documentation
    #value for 0.015 estimation of sensor position on arm
    trans =  np.array([0.05775+0.015,0,0.01231])
    result[:3,3] = trans
    return result




if __name__ == '__main__':
    UDP_PORT = 56200
    dataIO = DataIO(UDP_PORT) #create dataIO object
    dataIO.startProcess() #start data reading tread

    solver = Solver() #Create solver object

    startingPos = np.array([[ 0.14531189,  0.02731026,  0.9890089,   0.10855015],
                            [-0.98545492, -0.08502375,  0.14713755,  0.00251222],
                            [ 0.08810762, -0.99600452,  0.01455806,  0.11720823],
                            [ 0.,          0.,          0.,          1.        ]])

    nc = NaoController() #Create naoController object
    nc.setup(startingPosition=startingPos) #move robot arm to front to start moving

    #Create offset
    _,_,s1Input,s2Input,s3Input = dataIO.getFormattedData()
    offsetT = solver.solve(s1Input,s2Input,s3Input,normalize= False)
    offsetTRot = np.linalg.inv(offsetT[:3,:3])
    offsetTTrans = offsetT[:3,3] * -1

    while True:
        #Get transformation of left arm with respect to torso frame
        torso2Hand = nc.getOrientation('LArm')
        torso2HandRot = torso2Hand[:3,:3]
        torso2HandTrans = torso2Hand[:,3]
        wristYaw = nc.getlHandRotation()

        #Get data from sensor
        side,time,s1Input,s2Input,s3Input = dataIO.getFormattedData()
        print(time)
        sensT = solver.solve(s1Input,s2Input,s3Input,normalize= False)

        sensTRot = sensT[:3,:3]
        sensTTrans = sensT[:3,3]

        newSensTTrans = sensTTrans + offsetTTrans
        newSensTTrans[0] = getThresholdedValue(sensTTrans[0],0.002)*-3
        newSensTTrans[1] = 0.
        newSensTTrans[2] = 0.

        #GET the rotation
        newSensTRot = mm(sensTRot,offsetTRot)
        sensXr,sensYr,sensZr = getEuler3(sensTRot)

        sensXr = softClip(getThresholdedValue(sensXr,0.018),np.pi/3)/3
        sensYr = softClip(getThresholdedValue(sensYr,0.018),np.pi/3)/3
        sensZr = softClip(getThresholdedValue(sensZr,0.018),np.pi/3)/3

        newSensTRot = getRotMatFromEuler(np.array([0,sensYr,sensZr]))

        #Create new homogeneous sensor transform
        newSensT = np.identity(4)
        newSensT[:3,:3] = newSensTRot
        newSensT[:3,3] = newSensTTrans


        #Find new position for the hand
        a = mm(torso2Hand,np.linalg.inv(getHand2SensHom(wristYaw)))
        b = mm(a,np.linalg.inv(newSensT))
        c = mm(b,getHand2SensHom(wristYaw))

        nc.moveTo(c,interval=0.15)
