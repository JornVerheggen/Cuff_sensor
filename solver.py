
#%%
import numpy as np

def normalizeInputData(xyz, scaleFactor=50000) -> np.array:
    xyzPosNeg = np.absolute(xyz)/xyz
    xyz = 1/np.sqrt(np.absolute(xyz)) * xyzPosNeg * scaleFactor

def transformToRefrenceFrame(xyz,transformMatrix) -> np.array:
    return xyz @ transformMatrix

def getScale(xyz1,sens1,mag1,xyz2,sens2,mag2) -> np.array:
    return (mag1-mag2)/((sens1+xyz1) - (sens2+xyz2))

def getMagPosition(xyz,pos) -> np.array:
    return xyz + pos

def getTransrot(xyz1,xyz2,xyz3):
    pass

#%%
mag1TransfromMatix = np.matrix(
    [[np.cos(np.pi), -np.sin(np.pi),0],
    [np.sin(np.pi),   np.cos(np.pi),0],
    [ 0., 0., 1.] ])

mag2TransfromMatix = np.matrix(
    [[np.cos(np.pi/3), -np.sin(np.pi/3),0],
    [np.sin(np.pi/3),   np.cos(np.pi/3),0],
    [ 0., 0., 1.] ])

mag2TransfromMatix = np.matrix(
    [[np.cos(-np.pi/3), -np.sin(-np.pi/3),0],
    [np.sin(-np.pi/3),   np.cos(-np.pi/3),0],
    [ 0., 0., 1.] ])
# %%

sens1 = np.array([-34.2,0,0])
sens2 = np.array([17.1,29.618,0])
sens2 = np.array([17.1,-29.618,0])

mag1 = np.array([-47,0,0])
mag2 = np.array([23.5,40.7,0])
mag3 = np.array([23.5,-40.7,0])