import numpy as np
import math as m


def getRotmat4(axis,rad):
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

def getRotmat3(axis,rad):
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

def getEuler3(R):
    sy = m.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if  not singular :
        rx = m.atan2(R[2,1] , R[2,2])
        ry = m.atan2(-R[2,0], sy)
        rz = m.atan2(R[1,0], R[0,0])
    else :
        rx = m.atan2(-R[1,2], R[1,1])
        ry = m.atan2(-R[2,0], sy)
        rz = 0

    return (rx, ry, rz)

def getEuler4(R):
    x = R[0,3]
    y = R[1,3]
    z = R[2,3]

    R = R[:3,:3]

    rx, ry, rz = getEuler3(R)

    return (x, y, z, rx, ry, rz)


def getRotMatFromEuler(theta):
    R_x = np.array([[1, 0, 0 ],
    [0, m.cos(theta[0]), -m.sin(theta[0]) ],
    [0, m.sin(theta[0]), m.cos(theta[0]) ]
    ])

    R_y = np.array([[m.cos(theta[1]), 0, m.sin(theta[1]) ],
    [0, 1, 0 ],
    [-m.sin(theta[1]), 0, m.cos(theta[1]) ]
    ])

    R_z = np.array([[m.cos(theta[2]), -m.sin(theta[2]), 0],
    [m.sin(theta[2]), m.cos(theta[2]), 0],
    [0, 0, 1]
    ])

    R = np.dot(R_z, np.dot( R_y, R_x ))

    return R

def mm(a,b):
    return np.matmul(a,b)