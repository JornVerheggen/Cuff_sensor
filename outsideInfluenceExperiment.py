from modules.KRISHandler import KRISHandler
from modules.rotMat import getEuler4
from multiprocessing import Process
import numpy as np
import time as t

def homTrans2String(A):
    x,y,z,rx,ry,rz = getEuler4(A)
    result =  (str(x)  + ';')
    result += (str(y)  + ';')
    result += (str(z)  + ';')
    result += (str(rx) + ';')
    result += (str(ry) + ';')
    result += (str(rz) + '\n')
    return result

def naoRunner():
    from modules.naoController import NaoController
    nc = NaoController()

    base =     np.array([[ 0.97951078,  0.19790787, -0.03729767,  0.18621776],
                         [-0.19608623,  0.97943777,  0.04745132,  0.10159862],
                         [ 0.04592174, -0.03916552,  0.99817687,  0.02211484],
                         [ 0.        ,  0.        ,  0.        ,  1.        ]])

    right =    np.array([[ 0.76143301,  0.63996649, -0.10325956,  0.15688077],
                         [-0.62322402,  0.76652527,  0.15501875,  0.02482015],
                         [ 0.17835787, -0.05368255,  0.98250008,  0.02766118],
                         [ 0.        ,  0.        ,  0.        ,  1.        ]])

    left =     np.array([[ 0.88827699, -0.44554088, -0.11161256,  0.14922285],
                         [ 0.45373449,  0.88893741,  0.0625726 ,  0.17671253],
                         [ 0.07133793, -0.10622427,  0.99177992,  0.00492496],
                         [ 0.        ,  0.        ,  0.        ,  1.        ]])

    up =       np.array([[ 0.50154507,  0.0811446 , -0.86131757,  0.16801919],
                         [-0.08893348,  0.99515307,  0.04196727,  0.09119017],
                         [ 0.8605482 ,  0.05555148,  0.50633061,  0.15759484],
                         [ 0.        ,  0.        ,  0.        ,  1.        ]])

    down =     np.array([[ 0.72986841,  0.06968322,  0.68002677,  0.12850268,],
                         [-0.09704909,  0.99527717,  0.00217482,  0.09287015,],
                         [-0.67666352, -0.06758331,  0.73318404, -0.07712643,],
                         [ 0.        ,  0.        ,  0.        ,  1.        ,]])

    back =     np.array([[ 0.99954295, -0.02168957,  0.02105845,  0.11544158,],
                         [ 0.01999845,  0.99679637,  0.07744043,  0.12532535,],
                         [-0.02267064, -0.07698389,  0.99677455, -0.01765619,],
                         [ 0.        ,  0.        ,  0.        ,  1.        ,]])

    forward =  np.array([[ 0.99259257,  0.1064648 ,  0.05852627,  0.20487104,],
                         [-0.10749128,  0.99409783,  0.01467099,  0.09363957,],
                         [-0.0566189 , -0.02085338,  0.99817812,  0.03042427,],
                         [ 0.        ,  0.        ,  0.        ,  1.        ,]])

    path = [base,left,base,right,base,up,base,down,base,forward,base,back]

    nc.setup()
    print("run1: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run2: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run3: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run4: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run5: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run6: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run7: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run8: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run9: " + str(t.time()))
    nc.playPath(path,2.0)
    print("run10: " + str(t.time()))
    nc.playPath(path,2.0)
    print("end: " + str(t.time()))
    nc.rest()

if __name__ == "__main__":


    p = Process(target=naoRunner)
    p.start()

    kh = KRISHandler()

    fp1 = open('./data/outsideInfluenceExperiment/transFormData.csv', 'w')
    while True:
        rawInput = kh.getRawInput()
        line = str(t.time())+";"
        line += homTrans2String(rawInput)
        fp1.write(line)
        t.sleep(0.05)

    

        
