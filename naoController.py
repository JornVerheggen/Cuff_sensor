# -*- encoding: UTF-8 -*-

'''Cartesian control: Arm trajectory example'''
''' This example is only compatible with NAO '''
import motion
import almath
from naoqi import ALProxy

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
    
    def relativeMove(self,xyz):
        currentTf = self.motionProxy.getTransform(self.effector, self.frame, self.useSensorValues)
        targetTf  = almath.Transform(currentTf)
        targetTf.r1_c4 += float(xyz[0]) # x
        targetTf.r2_c4 += float(xyz[1]) # y
        targetTf.r3_c4 += float(xyz[2]) # z

        path = []
        path.append(list(targetTf.toVector()))

        times      = [.1] # seconds
        self.motionProxy.transformInterpolations(self.effector, self.frame, path, self.axisMask, times)
    
    def getOrientation(self,A):
        #chainName = A, worldFrame =1, useSensors = True
        return almath.Transform(self.motionProxy.getTransform(A, self.frame, True))
    
    def getlHandRotation(self):
        return self.memoryProxy.getData("Device/SubDeviceList/LWristYaw/Position/Sensor/Value")   
    
    def rest(self):
        self.motionProxy.rest()