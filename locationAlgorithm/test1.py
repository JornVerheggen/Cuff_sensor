import numpy as np



# def transS1ToReferenceFrame(S1):
#     return np.array([-S1[2],-S1[0],S1[1]])

# def transS2ToReferenceFrame(S2):
#     return np.array([S2[2],-S2[0],-S2[1]])


# #Get the input from the sensors
# sensorInput = input("Give sensor input: ")

# sensorInput = sensorInput.split('\t')
# for i, val in enumerate(sensorInput):
#     sensorInput[i] = float(val[4:])

# AJ = np.array(sensorInput[:3])
# BK = np.array(sensorInput[3:])

# #Transform the sensor valus to the reference frame of the inner ring
# #This needs to be done because the sensors cannot be mounted in the same orientation as the inner ring
# AJ = transS1ToReferenceFrame(AJ)
# BK = transS2ToReferenceFrame(BK)




AJ = np.array([-.3,0.,0.,],dtype=np.float32)
BK = np.array([.3,0.,0.,],dtype=np.float32)



#Define the distance between the sensors in the inner ring
#point O is defined as [0.0,0.0,0.0]

OA = np.array([-10,0,0], dtype = np.float32)
OB = np.array([10,0,0], dtype = np.float32)
JK = np.array([80,0,0], dtype = np.float32)


a = np.array([ 
    [-1 , 0, 0, 0, 0, 0, BK[0]],
    [0 , -1, 0, 0, 0, 0, BK[1]],
    [0 , 0, -1, 0, 0, 0, BK[2]],
    [0 , 0, 0, 1, 0, 0, AJ[0]],
    [0 , 0, 0, 0, 1, 0, AJ[1]],
    [0 , 0, 0, 0, 0, 1, AJ[2]],

])

b = np.array([  -JK[0]-OA[0],
                -JK[1]-OA[1],
                -JK[2]-OA[2],
                JK[0]-OB[0],
                JK[1]-OB[1],
                JK[2]-OB[2] ])

print(a.shape)
print(b.shape)

x = np.linalg.lstsq(a,b,rcond=None)

ans = x[0]

print(f' Xpos1: {ans[0]:.2f}, Ypos1: {ans[1]:.2f}, Zpos1: {ans[2]:.2f}\n Xpos2: {ans[3]:.2f}, Ypos2: {ans[4]:.2f}, Zpos2: {ans[5]:.2f}\n Magnet scale: {ans[6]:.2f}')