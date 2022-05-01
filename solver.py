
# %%
import numpy as np
import math as m
import cmath


def normalizeInputData(xyz, multiplier=50000) -> np.array:
    xyzPosNeg = np.absolute(xyz)/xyz
    xyz = 1/np.sqrt(np.absolute(xyz)) * xyzPosNeg * multiplier


def transformToRefrenceFrame(xyz, transformMatrix) -> np.array:
    return xyz @ transformMatrix


def getScale(sa, vsama, ma, sb, vsbmb, mb) -> np.array:

    print(vsama)
    dmamb = np.sqrt(np.sum(np.square(ma-mb)))
    #dmamb = 81.404
    print(dmamb)

    sxdif = sb[0] - sa[0]
    sydif = sb[1] - sa[1]
    szdif = sb[2] - sa[2]     

    vxdif = vsbmb[0] - vsama[0]
    vydif = vsbmb[1] - vsama[1]
    vzdif = vsbmb[2] - vsama[2]    

    print(f'here{vxdif}')
    #ABC formula

    a = 3

    b = 6 * (sxdif*vxdif+sydif*vydif+szdif*vzdif) + 6 *(vxdif + vydif + vzdif)

    c = - cmath.sqrt(dmamb) + sxdif**2 + sydif**2 + szdif**2 + vxdif**2 + vydif**2 + vzdif**2

    d = (b**2) - (4*a*c)

    # find two solutions
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)

    print(f'A is {a}, B is {b} and C is{c}')
    print('The solution are {0} and {1}'.format(sol1,sol2))


def getMagPosition(xyz, pos) -> np.array:
    return xyz + pos


def getTransrot(xyz1, xyz2, xyz3):
    pass

def getTransmat(num) -> np.array:
    if num == 1:
        return np.array(
        [[np.cos(np.pi), -np.sin(np.pi), 0],
        [np.sin(np.pi),   np.cos(np.pi), 0],
        [0., 0., 1.]])

    elif num == 2:
        return np.array(
        [[np.cos(np.pi/3), -np.sin(np.pi/3), 0],
        [np.sin(np.pi/3),   np.cos(np.pi/3), 0],
        [0., 0., 1.]])

    elif num == 3: 
        return np.array(
        [[np.cos(-np.pi/3), -np.sin(-np.pi/3), 0],
        [np.sin(-np.pi/3),   np.cos(-np.pi/3), 0],
        [0., 0., 1.]])

def getSp(num):
    if num == 1:
        return np.array([-34.2, 0, 0])
    elif num == 2:
        return np.array([17.1, 29.618, 0])
    elif num == 3:
        return np.array([17.1, -29.618, 0])

def getMp(num):
    if num == 1:
        return np.array([-47, 0, 0])
    elif num == 2:
        return np.array([23.5, 40.7, 0])
    elif num == 3:
        return np.array([23.5, -40.7, 0])

