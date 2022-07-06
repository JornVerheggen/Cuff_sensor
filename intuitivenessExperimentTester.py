from modules.naoController import NaoController
from modules.dataIO import DataIO
from modules.solver import Solver
from modules.keyBoardHandler import KeyboardHandler
from modules.rotMat import getEuler4

import time as t
import numpy as np
import os

leg = np.array([[ 0.49924511,  0.20212385,  0.84255576,  0.06828849],
                [-0.51835829,  0.84887642,  0.10350606,  0.04647925],
                [-0.69430465, -0.48842067,  0.52857,    -0.0888659 ],
                [ 0.,          0.,          0.,          1.        ]])
 
forward = np.array([[ 0.98677087,  0.13854256, -0.08419752,  0.21614906],
                    [-0.12485236,  0.98070091,  0.15045753,  0.10732553],
                    [ 0.10341736, -0.13795485,  0.98502445,  0.09584652],
                    [ 0.,          0.,          0.,          1.        ]])
 
head = np.array([   [-2.43755847e-01,  7.88690090e-01,  5.64403355e-01, -9.17481259e-04],
                    [-7.55151153e-01, -5.19509971e-01,  3.99820179e-01,  2.92607211e-02],
                    [ 6.08547330e-01, -3.28751326e-01,  7.22213805e-01,  2.58410245e-01],
                    [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])

chest = np.array(  [[ 0.34482086, -0.11369565,  0.93175745,  0.10544825],
                    [-0.90468723, -0.30492294,  0.29759532, -0.00861193],
                    [ 0.25027892, -0.94556618, -0.20800279,  0.05883116],
                    [ 0.,          0.,          0.,          1.        ]])
 
out = np.array(    [[ 0.33778086,  0.77233481, -0.53796196,  0.12489316,],
                    [ 0.44581023,  0.37209487,  0.81412452,  0.1893073, ],
                    [ 0.82894963, -0.51482463, -0.21862823,  0.1489107, ],
                    [ 0.,          0.,          0.,          1.,        ]])

#DEFINE FREEMOVE FUNCTIONS
def feeMoveKeyboard():
    newPosition = nc.getOrientation('LArm')
    adjustment = keyboardHandler.getSingleTransform()
    nextPosition = np.matmul(adjustment,newPosition)
    nc.moveTo(nextPosition)
    return adjustment

def freeMoveKRIS():
    pass

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


#SETTINGS   
positionIndex = 4             
positions = [leg,forward,head,chest,out]
position = positions[positionIndex] #Position 0 t/m 4
#method = "KRIS"
method = "keyboard"
# method = "touch"
assert method == 'touch' or method == 'keyboard' or method == 'KRIS'

participant = 0 #number
timeout = 45 #seconds
closeNessFactor = 0.05 #meters
success = False

#LOAD MODULES
nc = NaoController()
if method == "KRIS":
    dataIO = DataIO()
    solver = Solver()
if method == 'keyboard':
    keyboardHandler = KeyboardHandler()

#SETUP EXPERIMENT
path = "./data/"+str(participant)+ '/'
if not os.path.isdir(path):
    os.mkdir(path)

if method == 'KRIS':
    inputFp = open(path +'KRISinputData.csv','w+')
    outputFp = open(path +'KRISOutputData.csv','w+')

if method == 'keyboard':
    inputFp = open(path +'keyboardinputData.csv','w+')
    outputFp = open(path +'keyboardOutputData.csv','w+')

if method == 'touch':
    outputFp = open(path +'touchOputData.csv','w+')

nc.setup()
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
resultFp = open(path+ method + 'result.txt','w+')

if success:
    resultFp.write("P.\n") #Pass
    resultFp.write(str(successTime))
else:
    nc.say("Timeout reached")
    resultFp.write("F.\n") #Fail

resultFp.close()
nc.rest()
print("Experiment finished")