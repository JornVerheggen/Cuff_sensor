import numpy as np

AJ = np.array([-30,1.,0.,],dtype=np.float32)
BK = np.array([30.,-1.,0.,],dtype=np.float32)


A = np.array([-10,0,0], dtype = np.float32)
B = np.array([10,0,0], dtype = np.float32)


a = np.array([ 
    [-1 , 0, 0, 0, 0, 0, AJ[0]],
    [0 , -1, 0, 0, 0, 0, AJ[1]],
    [0 , 0, -1, 0, 0, 0, AJ[2]],
    [0 , 0, 0, -1, 0, 0, BK[0]],
    [0 , 0, 0, 0, -1, 0, BK[1]],
    [0 , 0, 0, 0, 0, -1, BK[2]],
    [-1,-1,-1,1,1,1,0],

])


b = np.array([  -A[0],
                -A[1],
                -A[2],
                -B[0],
                -B[1],
                -B[2],
                80])


x = np.linalg.lstsq(a,b,rcond=None)

ans = x[0]

print(f' Xpos1: {ans[0]:.2f}, Ypos1: {ans[1]:.2f}, Zpos1: {ans[2]:.2f}\n Xpos2: {ans[3]:.2f}, Ypos2: {ans[4]:.2f}, Zpos2: {ans[5]:.2f}\n Magnet scale: {ans[6]:.2f}')

ABdist = ((ans[3]-ans[0])**2  +  (ans[4] - ans[1])**2  +  (ans[5] - ans[2])**2)**.5

print(ABdist)

calca = ans[:3]
calcb = ans[3:6]

mean = (calcb-calca) /2

scale = 80/ABdist

adja = ((calca-mean) * scale) + mean
adjb = ((calcb-mean) * scale) + mean

print(adja)
print(adjb)

print(f' Xpos1: {ans[0]:.2f}, Ypos1: {ans[1]:.2f}, Zpos1: {ans[2]:.2f}\n Xpos2: {ans[3]:.2f}, Ypos2: {ans[4]:.2f}, Zpos2: {ans[5]:.2f}\n Magnet scale: {ans[6]:.2f}')