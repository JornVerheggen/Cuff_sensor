from ipaddress import ip_address
from modules.KRISHandler import KRISHandler
from modules.naoController import NaoController
from modules.dataIO import DataIO
from modules.solver import Solver
from modules.keyBoardHandler import KeyboardHandler
from modules.rotMat import getEuler4 ,mm

import time as t
import numpy as np
import os

start = np.array([[ 0.39880186, -0.18449461,  0.89828658,  0.09819493],
                   [-0.89091223,  0.15419865,  0.42719802,  0.00965391],
                   [-0.21733031, -0.97066188, -0.1028738 , -0.00611237],
                   [ 0.        ,  0.        ,  0.        ,  1.        ]])

inside = np.array([[ 0.0116705 ,  0.41214985,  0.91104132,  0.09387776],
                    [-0.64348042, -0.69428641,  0.32233417,  0.00313159],
                    [ 0.76537359, -0.58999908,  0.2571077 ,  0.19682246],
                    [ 0.        ,  0.        ,  0.        ,  1.        ]])

outside = np.array([[ 0.24125169, -0.97039074,  0.01180979,  0.03397589],
                    [ 0.17865855,  0.05637149,  0.98229492,  0.21163194],
                    [-0.9538756 , -0.23487039,  0.18696833, -0.02044525],
                    [ 0.        ,  0.        ,  0.        ,  1.        ]])

#DEFINE FREEMOVE FUNCTIONS
def feeMoveKeyboard():
    newPosition = nc.getOrientation('LArm')
    adjustment = keyboardHandler.getSingleTransform()
    nextPosition = np.matmul(adjustment,newPosition)
    nc.moveTo(nextPosition)
    return adjustment

def freeMoveKRIS():
    nextPosition = KRISHandler.getSingleTransform()
    currentPosition = nc.getOrientation('LArm')
    nc.moveTo(nextPosition)

    return mm(np.linalg.inv(currentPosition),nextPosition)

#DEFINE HELPER FUNCTIONS
def closeTo(A,B,threshold):
    dist = ((A[0,3] - B[0,3])**2 + (A[1,3] - B[1,3])**2 +(A[2,3] - B[2,3])**2)**.5
    if dist <= threshold:
        return True
    else:
        return False

def homTrans2String(A):
    x,y,z,rx,ry,rz = getEuler4(A)
    result =  (str(x)  + ';')
    result += (str(y)  + ';')
    result += (str(z)  + ';')
    result += (str(rx) + ';')
    result += (str(ry) + ';')
    result += (str(rz) + '\n')
    return result

if __name__ == "__main__":

    #SETTINGS   
    print("Tester -- ")
    print("Positions, 0 - 1")
    positionIndex = raw_input('Position number: ')
    positionIndex = int(positionIndex)
    positions = [inside,outside]
    position = positions[positionIndex] #Position 0 t/m 4

    method = raw_input("Type of demonstration: \'touch\' \'keyboard\' or \'KRIS\' ")
    print("Demo type is: " + method)

    participantNumber = raw_input('Participant number: ')
    assert positionIndex == 1 or positionIndex == 0
    assert method == 'touch' or method == 'keyboard' or method == 'KRIS'

    timeout = 45 #seconds
    closeNessFactor = 0.05 #meters
    success = False

    #LOAD MODULES

    if method == "KRIS":
        KRISHandler = KRISHandler()
        nc = NaoController()
        t.sleep(1)
    if method == 'keyboard':
        keyboardHandler = KeyboardHandler()
        nc = NaoController(ip_address = "192.168.0.1")

    #SETUP EXPERIMENT
    path = "C:/Users/jorn-/Documents/school/y2/thesis/cuffling/code/Cuff_sensor/data/IntuitivenessExperiment/"+str(participantNumber)+ '/'
    if not os.path.isdir(path):
        os.mkdir(path)

    if method == 'KRIS':
        inputFp = open(path +'Pos' + str(positionIndex) + 'KRISInput.csv','w+')
        outputFp = open(path +'Pos' + str(positionIndex) +'KRISOutput.csv','w+')

    if method == 'keyboard':
        inputFp = open(path +'Pos' + str(positionIndex) +'keyboardInput.csv','w+')
        outputFp = open(path +'Pos' + str(positionIndex) +'keyboardOutput.csv','w+')

    if method == 'touch':
        outputFp = open(path +'Pos' + str(positionIndex) +'touchOutput.csv','w+')

    nc.setup(startingPosition=start)
    if method == 'touch':
        nc.setStiffness(0.0)
    startTime = t.time()


    #start training loop
    print("training loop started")
    while t.time() < startTime+timeout:
        if method == "KRIS":
            input = freeMoveKRIS()
        elif method == "keyboard":
            input = feeMoveKeyboard()
        elif method == 'touch':
            t.sleep(.05)
        output = nc.getOrientation('LArm')

        if method != 'touch':
            inputFp.write(homTrans2String(input))
        outputFp.write(homTrans2String(output))

        if closeTo(output,position,closeNessFactor):
            success = True
            successTime =  t.time() - startTime
            nc.say("Success")
            break

    if method != 'touch':
        inputFp.close()
    outputFp.close()
    resultFp = open(path + 'Pos' +str(positionIndex) + method + 'Result.txt','w+')

    if success:
        resultFp.write("P.\n") #Pass
        resultFp.write(str(successTime))
    else:
        nc.say("Timeout reached")
        resultFp.write("F.\n") #Fail

    resultFp.close()
    nc.rest()
    print("Experiment finished")