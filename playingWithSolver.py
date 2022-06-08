from math import degrees
from solver import Solver
import numpy as np
from scipy.spatial.transform import Rotation
import math


def RotMat(axis,rad):

    if axis == 'x':
        return np.array([[1.,0.,0.],
                        [0.,np.cos(rad),-np.sin(rad)],
                        [0.,np.sin(rad),np.cos(rad)]])
    elif axis == 'y':
        return np.array([[np.cos(rad),0,np.sin(rad)],
                        [0,1,0],
                        [-np.sin(rad),0,np.cos(rad)]])
    elif axis == 'z':
        return np.array([[np.cos(rad), -np.sin(rad), 0],
                        [np.sin(rad),   np.cos(rad), 0],
                        [0., 0., 1.]])


# rm = RotMat('x',.1) #@  RotMat('y',3)

s1 = Solver()

# a = np.stack([s1.mp1,s1.mp2,s1.mp3])


# b = np.stack([s1.mp1@rm,s1.mp2@rm,s1.mp3@rm])

# rotationObject, _ = Rotation.align_vectors(a,b)

# rot = rotationObject.as_rotvec('xyz')
# rot = [math.radians(x) for x in rot]

# print(rot)

a = np.array([[1,2,3],[5,6,7],[9,10,11]])
b = np.array([4,8,12])
print(s1.getHomogeneousTransform(a,b))
