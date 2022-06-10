import numpy as np 
from naoController import naoController
import math as m
import time as t
import keyboard

def getRotMat(axis,rad):

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
    naoController = naoController() #Create naoController object
    #move robot arm to front to start moving
    naoController.setup()

    radiansPerStep = m.radians(3)
    meterPerSep = .01

    while(True):
        if keyboard.is_pressed("up arrow"):
            up = True
        else:
            up = False

        if keyboard.is_pressed("down arrow"):
            down = True
        else:
            down = False

        if keyboard.is_pressed("left arrow"):
            left = True
        else:
            left = False

        if keyboard.is_pressed("right arrow"):
            right = True
        else:
            right = False

        if keyboard.is_pressed("right shift"):
            rightShift = True
        else:
            rightShift = False

        if keyboard.is_pressed("/"):
            slash = True
        else:
            slash = False

        if keyboard.is_pressed("w"):
            w = True
        else:
            w = False

        if keyboard.is_pressed("s"):
            s = True
        else:
            s = False

        if keyboard.is_pressed("d"):
            d = True
        else:
            d = False

        if keyboard.is_pressed("a"):
            a = True
        else:
            a = False

        newPosition = naoController.getOrientation('LArm')

        if rightShift and not slash:
            newPosition[0,3] += meterPerSep

        if slash and not rightShift:
            newPosition[0,3] -= meterPerSep

        if left and not right:
            newPosition[1,3] += meterPerSep

        if right and not left:
            newPosition[1,3] -= meterPerSep

        if up and not down:
            newPosition[2,3] += meterPerSep

        if down and not up:
            newPosition[2,3] -= meterPerSep
        
        if a and not d:
            newPosition = np.matmul(getRotMat('z',radiansPerStep),newPosition)

        if d and not a:
            newPosition = np.matmul(getRotMat('z',-radiansPerStep),newPosition)

        if w and not s:
            newPosition = np.matmul(getRotMat('y',radiansPerStep),newPosition)

        if s and not w:
            newPosition = np.matmul(getRotMat('y',-radiansPerStep),newPosition)

        naoController.moveTo(newPosition)