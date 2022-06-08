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


    def setup(self):
        # Wake up robot
        self.motionProxy.wakeUp()
        # Send robot to Stand Init
        self.postureProxy.goToPosture("StandInit", 0.5)

        path = []
        currentTf = self.motionProxy.getTransform(self.effector, self.frame, self.useSensorValues)
        targetTf  = almath.Transform(currentTf)
        targetTf.r1_c4 += 0.1 # x
        targetTf.r3_c4 += 0.18 # z

        path.append(list(targetTf.toVector()))

        # Go to the target and back again
        times      = [2.0] # seconds

        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)
    
    def relativeMove(self,transform):
        transform = transform.reshape((16,))
        transform = [float(x) for x in transform]
        path = [transform]
        times      = [.2] # seconds

        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)
    
    def getOrientation(self,A):
        #chainName = A, worldFrame =1, useSensors = True
        return np.array(self.motionProxy.getTransform(A, self.frame, True)).reshape((4,4))
    
    def getlHandRotation(self):
        return self.memoryProxy.getData("Device/SubDeviceList/LWristYaw/Position/Sensor/Value")   
    
    def rest(self):
        self.motionProxy.rest()