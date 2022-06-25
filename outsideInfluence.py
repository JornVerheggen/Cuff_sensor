import numpy as np
from naoController import naoController
from multiprocessing import Process
from dataIO import dataIO
from solver import Solver
from scipy.spatial.transform import rotation
import time as t
import math


def rotationMatrixToEulerAngles(R) :
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
    return np.array([x, y, z])

def naoRunner():
    nc = naoController()
    path = [
        np.array([[ 0.79884082, -0.35174501,  0.48798442,  0.0954641 ],
            [-0.21822879,  0.58649635,  0.7799989 ,  0.07648443],
            [-0.56056178, -0.7295872 ,  0.39175633, -0.07329781],
            [ 0.        ,  0.        ,  0.        ,  1.        ]]),
        np.array([[ 0.36628917,  0.05258733, -0.92901385,  0.11161593],
            [ 0.30095661,  0.93804264,  0.17175883,  0.20950635],
            [ 0.88048691, -0.34250623,  0.32776836,  0.15709892],
            [ 0.        ,  0.        ,  0.        ,  1.        ]]),
        np.array([[ 0.28894848,  0.19949877, -0.93632746,  0.14128694],
            [-0.47161183,  0.88079935,  0.0421294 ,  0.02567818],
            [ 0.83312142,  0.42940986,  0.34859163,  0.15133962],
            [ 0.        ,  0.        ,  0.        ,  1.        ]]),
        np.array([[ 0.9618299 , -0.0883936 ,  0.2589781 ,  0.1385892 ],
            [-0.12405667,  0.70270324,  0.70058405,  0.14787301],
            [-0.24391189, -0.70597064,  0.66491514, -0.00611768],
            [ 0.        ,  0.        ,  0.        ,  1.        ]])]

    nc.setup()
    nc.playPath(path,2.0)
    nc.rest()

if __name__ == "__main__":
    p = Process(target=naoRunner)
    p.start()

    # UDP_PORT = 56200
    # dataIO = dataIO(UDP_PORT) #create dataIO object
    # dataIO.startProcess() #start data reading tread

    # solver = Solver() #Create solver object

    # fp1 = open("ousideInfluence.csv",'w')
    # fp1.write("t;x;y;z;rx;ry;rz\n")

    # while True:
    #     side,time,s1Input,s2Input,s3Input = dataIO.getFormattedData()
    #     sensT = solver.solve(s1Input,s2Input,s3Input,normalize= False)

    #     x = sensT[0,3]
    #     y = sensT[1,3]
    #     z = sensT[2,3]

    #     rotmat = sensT[:3,:3]
    #     r = rotationMatrixToEulerAngles(rotmat)

    #     rx = r[0]
    #     ry = r[1]
    #     rz = r[2]
    #     fp1.write(str(time)+';'+str(x)+';'+str(y)+';'+str(z)+';'+str(rx)+';'+str(ry)+';'+str(rz)+';\n')
        
    #     t.sleep(0.05)
        
