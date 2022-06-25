import keyboard
import math as m
import numpy as np
import time as t


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


class KeyboardHandler:

    def __init__(self):
        self.radPerSep =  m.radians(5) # 3degrees
        self.mPerStep = .01 # 1mm
        self.collectionCounter = 0
        self.xyz = [0,0,0]
        self.rxyz = [0,0,0]

    def getKeyboardInfo(self):

        result = {
            'x': 0,
            'y': 0,
            'z': 0,
            'rx': 0,
            'ry': 0,
            'rz': 0,
        }

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

        if rightShift and not slash:
            result['x'] = 1

        if slash and not rightShift:
            result['x'] = -1

        if left and not right:
            result['y'] = 1

        if right and not left:
            result['y'] = -1

        if up and not down:
            result['z'] = 1

        if down and not up:
            result['z'] = -1
        
        if a and not d:
            result['rz'] = 1

        if d and not a:
            result['rz'] = -1

        if w and not s:
            result['ry'] = 1

        if s and not w:
            result['ry'] = -1

        return result

    def getModTransform(self,xyz,rxyz):
        newTransform = np.identity(4)

        newTransform = np.matmul(newTransform,getRotMat('x',xyz[0]*self.radPerStep))
        newTransform = np.matmul(newTransform,getRotMat('y',xyz[1]*self.radPerStep))
        newTransform = np.matmul(newTransform,getRotMat('z',xyz[2]*self.radPerStep))

        trans = np.identity(4)
        trans[0,3] = rxyz[0] * self.mPerStep
        trans[1,3] = rxyz[1] * self.mPerStep
        trans[2,3] = rxyz[2] * self.mPerStep

        newTransform = np.matmul(newTransform,trans)
    
    def collectInput(self):

        if self.collectionCounter > 0:
            xyz  = []
            rxyz = []
            for i in self.xyz:
                xyz.append((float(i)/self.collectionCounter) * self.mPerStep)
            for i in self.rxyz:
                rxyz.append((float(i)/self.collectionCounter) * self.radPerSep)
        else:
            xyz = [0,0,0]
            rxyz = [0,0,0]

        self.collectionCounter = 0
        self.xyz = [0,0,0]
        self.rxyz = [0,0,0]



        return (xyz,rxyz)

    def gatherInput(self):
        self.collectionCounter += 1 
        keyBoardInput = self.getKeyboardInfo()
        self.xyz[0] += keyBoardInput['x']
        self.xyz[1] += keyBoardInput['y']
        self.xyz[2] += keyBoardInput['z']

        self.rxyz[0] += keyBoardInput['rx']
        self.rxyz[1] += keyBoardInput['ry']
        self.rxyz[2] += keyBoardInput['rz']