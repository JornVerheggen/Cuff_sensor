from modules.keyBoardHandler import KeyboardHandler
from modules.policy import circlePolicy
import time as t
import math as m
from multiprocessing import Process, Queue
import numpy as np

#Used to not block the tread 
def batchHandler(queue,startPos):
    from modules.naoController import NaoController
    nc = NaoController()
    nc.setup(startingPosition=startPos)

    while True:
        if not queue.empty():
            path,times = queue.get()
        try:
            nc.playInterval(path,times)
        except:
            pass
        

if __name__ == "__main__":
    keyboardHandler = KeyboardHandler()
    batchSize = 10
    xyz = [0,0,0]

    center = (0.1695,0.083,0.15)
    policy = circlePolicy(center,.1,.1,0.0,m.radians(100),0.15)
    policy.createPath()
    timePerStep = policy.sampleTime
    startPos = policy.path[0]

    queue = Queue()

    #
    times = [timePerStep]
    for i in range(batchSize-1):
        times.append(times[-1]+timePerStep)

    p = Process(target=batchHandler,args=([queue,startPos]))
    p.start()
    t.sleep(.2)

    while True:

        #split path up into batches
        for i in range(0,len(policy.path),batchSize):
            startBatch = i
            endBatch = i + batchSize
            #print("Iteration: "+str(iteration)+", Batch: ("+str(startBatch) + '-' + str(endBatch)+')/'+str(len(policy.path)))

            #prepare new movement command
            path = policy.path[startBatch:endBatch]
            path = [list(x.reshape((16,))) for x in path]
            for j in range(len(path)):
                for k in range(len(path[j])):
                    path[j][k] = float(path[j][k])

            #send new movement command
            newBatch = (path,times[:len(path)])

            #Collect update info
            while not queue.empty():
                keyboardHandler.gatherInput()

            xyz, _ = keyboardHandler.collectInput()
            if xyz[0] != 0.0 or xyz[1]!= 0.0 or xyz[2] != 0.0:
                policy.updatePath(xyz,q)

            q = min(int(startBatch/(len(policy.path)/4)) + 1,4)
            print("Q: "+str(q) + ", Width "+str(policy.width)+", Height: "+str(policy.height),", Pitch: "+str(m.degrees(policy.pitch)))

            queue.put(newBatch)
