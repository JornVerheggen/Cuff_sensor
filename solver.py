import numpy as np


def normalizeInputData(xyz, multiplier=50000) -> np.array:
    xyzPosNeg = np.absolute(xyz)/xyz
    xyz = 1/np.sqrt(np.absolute(xyz)) * xyzPosNeg * multiplier

def transformToRefrenceFrame(xyz, transformMatrix) -> np.array:
    return transformMatrix @ xyz

def getScaleFactor(sa, vsama, ma, sb, vsbmb, mb) -> np.array:
    return (-sa - (mb-ma) + sb) / (vsama-vsbmb)

def getMeanScaleFactor(sf12,sf23,sf31) -> float:
    return np.nanmean(np.concatenate((sf12,sf23,sf31)))

def getMagPosition(sensorPos, vector, sf) -> np.array:
    return sensorPos + vector * sf

def getTranslation(m1, m2, m3) -> np.array:
    return  (m1+m2+m3) / 3

def getRotation(m1, m2, m3) -> np.array:

    N = np.cross((m1-m3),(m2-m3))
    U = N/ np.linalg.norm(N)

    return np.pi/2 - np.arccos(U)

def getRotMat(num) -> np.array:
    if num == 1: # -90deg y-axis -> 180deg z-axis
        return np.array([
            [np.cos(-np.pi/2),0,np.sin(-np.pi/2)],
            [0,1,0],
            [-np.sin(-np.pi/2),0,np.cos(-np.pi/2)]]) @ \
            np.array(
            [[np.cos(np.pi), -np.sin(np.pi), 0],
            [np.sin(np.pi),   np.cos(np.pi), 0],
            [0., 0., 1.]])
    elif num == 2: #120deg z-axis -> -90deg y-axais
        return np.array(
            [[np.cos(np.pi/1.5), -np.sin(np.pi/1.5), 0],
            [np.sin(np.pi/1.5),   np.cos(np.pi/1.5), 0],
            [0., 0., 1.]]) @ \
            np.array([
            [np.cos(-np.pi/2),0,np.sin(-np.pi/2)],
            [0,1,0],
            [-np.sin(-np.pi/2),0,np.cos(-np.pi/2)]])
    elif num == 3: #-120deg z-axis -> -90deg y-axis
        return np.array(
            [[np.cos(-np.pi/1.5), -np.sin(-np.pi/1.5), 0],
            [np.sin(-np.pi/1.5),   np.cos(-np.pi/1.5), 0],
            [0., 0., 1.]]) @ \
            np.array([
            [np.cos(-np.pi/2),0,np.sin(-np.pi/2)],
            [0,1,0],
            [-np.sin(-np.pi/2),0,np.cos(-np.pi/2)]])

def getSp(num):
    if num == 1:
        return np.array([-34.2, 0, 0])
    elif num == 2:
        return np.array([17.1, -29.6180688, 0])
    elif num == 3:
        return np.array([17.1, 29.6180688, 0])

def getMp(num):
    if num == 1:
        return np.array([-47, 0, 0])
    elif num == 2:
        return np.array([23.5, -40.7031939, 0])
    elif num == 3:
        return np.array([23.5, 40.7031939, 0])