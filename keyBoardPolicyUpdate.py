import numpy as np
import keyboard
from naoController import naoController
from policy import Policy
import time as t
import math as m
from multiprocessing import Process, Queue

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

def getKeyboardInfo():

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

def getModTransform(input):
    radiansPerStep = m.radians(3)
    meterPerSep = .01

    newTransform = np.identity(4)

    newTransform = np.matmul(newTransform,getRotMat('x',input['rx']*radiansPerStep))
    newTransform = np.matmul(newTransform,getRotMat('y',input['ry']*radiansPerStep))
    newTransform = np.matmul(newTransform,getRotMat('z',input['rz']*radiansPerStep))

    trans = np.identity(4)
    trans[0,3] = input['x'] * meterPerSep
    trans[1,3] = input['y'] * meterPerSep
    trans[2,3] = input['z'] * meterPerSep

    newTransform = np.matmul(newTransform,trans)

    return newTransform

def batchHandler(queue):
    from naoController import naoController
    naoController = naoController()
    naoController.setup()

    while True:
        if not queue.empty():
            path,times = queue.get()
        naoController.playInterval(path,times)
        

if __name__ == "__main__":
    numberOfIterations = 10
    batchSize = 5
    timePerStep = 0.03


    policy = Policy()
    policy.loadPath('whisky')

    queue = Queue()

    #sampleTime 0.1, batchSize 5
    times = [timePerStep]
    for i in range(batchSize-1):
        times.append(times[-1]+timePerStep)

    p = Process(target=batchHandler,args=([queue]))
    p.start()

    for iteration in range(numberOfIterations):
        for i in range(0,len(policy.path),batchSize):
            startBatch = i
            endBatch = i + batchSize
            print("Iteration: "+str(iteration)+" Batch: "+str(startBatch) + ' t/m ' + str(endBatch))

            path = policy.path[startBatch:endBatch]
            path = [list(x.reshape((16,))) for x in path]
            for i in range(len(path)):
                for j in range(len(path[i])):
                    path[i][j] = float(path[i][j])

            newBatch = (path,times)
            queue.put(newBatch)
            isUpdated = False
            while not queue.empty():
                if not isUpdated:
                    info = getKeyboardInfo()
                    transform = getModTransform(info)
                    for j in range(startBatch,endBatch):
                        policy.path[j] = np.matmul(policy.path[j],transform) 
                    isUpdated = True
                        



