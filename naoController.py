# -*- encoding: UTF-8 -*-

'''Cartesian control: Arm trajectory example'''
''' This example is only compatible with NAO '''
import motion
import almath
from naoqi import ALProxy
import numpy as np

class naoController:

    def __init__(self,robotIP='192.168.0.210',PORT=9559):

        self.motionProxy  = ALProxy("ALMotion", robotIP, PORT)
        self.postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
        self.memoryProxy = ALProxy("ALMemory", robotIP, PORT)
        self.effector   = "LArm"
        self.frame      = motion.FRAME_TORSO
        self.axisMask   = almath.AXIS_MASK_VEL # just control position
        self.useSensorValues = False


    def setup(self,stiff = True, startingPosition = None):
        # Wake up robot
        self.motionProxy.wakeUp()
        # Send robot to Stand Init
        self.postureProxy.goToPosture("StandInit", 0.5)

        path = []

        if startingPosition is None:
            targetTf = np.identity(4)

            targetTf[0,3] = 0.218
            targetTf[1,3] = 0.113
            targetTf[2,3] = 0.11231
        
        else:
            targetTf = startingPosition

        targetTf = targetTf.reshape((16,))
        targetTf = [float(x) for x in targetTf]
        path = [targetTf]

        times = [3.0] # seconds

        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)

        if not stiff:
            self.motionProxy.stiffnessInterpolation(self.effector, 0.0, 1.0)
    
    def moveTo(self,transform, interval = 0.1):
        transform = transform.reshape((16,))
        transform = [float(x) for x in transform]
        path = [transform]
        times      = [interval] # seconds

        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)

    def playPath(self,path,sampleTime):
        times = [sampleTime]
        for i in range(1,len(path)):
            times.append(times[-1]+sampleTime)

        path = [list(x.reshape((16,))) for x in path]
        for i in range(len(path)):
            for j in range(len(path[i])):
                path[i][j] = float(path[i][j])

        self.motionProxy.stiffnessInterpolation(self.effector, 1.0, 1.0)
        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)
    
    def playInterval(self,path,times):
        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)

    def getOrientation(self,A):
        #chainName = A, worldFrame =1, useSensors = True
        return np.array(self.motionProxy.getTransform(A, self.frame, False)).reshape((4,4))
    
    def getlHandRotation(self):
        return self.memoryProxy.getData("Device/SubDeviceList/LWristYaw/Position/Sensor/Value")   
    
    def rest(self):
        self.motionProxy.rest()