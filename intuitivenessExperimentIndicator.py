from modules.naoController import NaoController
import time as t
import numpy as np

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

#SETUP
positions = [inside,outside]
print("Positions, 0 - 1")
positionIndex = int(raw_input('Position number: '))
nc = NaoController(robotIP = '192.168.0.238')

nc.setup(startingPosition=positions[positionIndex])

while True:
    if nc.getFootBumper():
        break

nc.rest()


