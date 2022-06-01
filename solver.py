import numpy as np

class Solver:

    def __init__(self):
        #define sensor positions
        self.sp1 = np.array([-34.2, 0, 0])
        self.sp2 = np.array([17.1, -29.6180688, 0])
        self.sp3 = np.array([17.1,  29.6180688, 0])
    
        #define magnet positions without any rotation/translation
        self.mp1 = np.array([-47, 0, 0])
        self.mp2 = np.array([23.5, -40.7031939, 0])
        self.mp3 = np.array([23.5,  40.7031939, 0])

        #define sensor rotation matrices
            # 90deg y-axis -> 180deg z-axis
        self.rm1 = np.matmul(np.array(
                [[np.cos(np.pi), -np.sin(np.pi), 0],
                [np.sin(np.pi),   np.cos(np.pi), 0],
                [0., 0., 1.]]) , \
                np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]]))
            # 90deg y-axis -> -60deg z-axis
        self.rm2 = np.matmul(np.array(
                [[np.cos(-np.pi/3), -np.sin(-np.pi/3), 0],
                [np.sin(-np.pi/3),   np.cos(-np.pi/3), 0],
                [0., 0., 1.]]) , \
                np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]]))

            # 90deg y-axis -> 60deg z-axis
        self.rm3 = np.matmul(np.array(
                [[np.cos(np.pi/3), -np.sin(np.pi/3), 0],
                [np.sin(np.pi/3),   np.cos(np.pi/3), 0],
                [0., 0., 1.]]) , \
                np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]]))
            
            #90deg y-axis
        self.rm4 = np.array([
                [np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]])

    def solve(self, s1Input,s2Input,s3Input,normalize=True):
        if normalize:
            #Invert the z-axis so that value increases as magnet goes farther away from the sensor
            s1NormInput = s1Input
            s1NormInput[2] =  (s1Input[2] * -1) + 53000
            s2NormInput = s2Input
            s2NormInput[2] =  (s1Input[2] * -1) + 53000
            s3NormInput = s3Input
            s3NormInput[2] =  (s1Input[2] * -1) + 53000
        else: 
            s1NormInput = s1Input            
            s2NormInput = s2Input            
            s3NormInput = s3Input

        #print(f"S1 normalization: {s1Input[2]} --> {s1NormInput[2]}")

        v1 =  self.transformToRefrenceFrame(s1NormInput,self.rm1)
        v2 =  self.transformToRefrenceFrame(s2NormInput,self.rm2)
        v3 =  self.transformToRefrenceFrame(s3NormInput,self.rm3)

        sf12 = self.getScaleFactor(self.sp1,v1,self.mp1,self.sp2,v2,self.mp2)
        sf23 = self.getScaleFactor(self.sp2,v2,self.mp2,self.sp3,v3,self.mp3)
        sf31 = self.getScaleFactor(self.sp3,v3,self.mp3,self.sp1,v1,self.mp1)

        sf = self.getMeanScaleFactor(sf12,sf23,sf31)

        m1Pos = self.getMagPosition(self.sp1,v1,sf)
        m2Pos = self.getMagPosition(self.sp2,v2,sf)
        m3Pos = self.getMagPosition(self.sp3,v3,sf)

        outerPos = self.getTranslation(m1Pos,m2Pos,m3Pos)

        outerRot = self.getRotation(m1Pos,m2Pos,m3Pos)

        return (outerPos,outerRot)

    def normalizeInputData(self, xyz, multiplier=50000):
        xyzPosNeg = np.absolute(xyz)/xyz
        res = 1/np.sqrt(np.absolute(xyz)) * xyzPosNeg * multiplier
        return res

    def transformToRefrenceFrame(self,xyz, transformMatrix):
        return np.matmul(transformMatrix, xyz)

    def getScaleFactor(self, sa, vsama, ma, sb, vsbmb, mb):
        factors = (-sa - (mb-ma) + sb) / (vsama-vsbmb)
        mask = np.isclose(factors,0)
        factors[mask] = np.nan
        return factors

    def getMeanScaleFactor(self, sf12,sf23,sf31):
        return np.nanmean(np.concatenate((sf12,sf23,sf31)))

    def getMagPosition(self, sensorPos, vector, sf):
        return sensorPos + vector * sf

    def getTranslation(self, m1, m2, m3):
        return  (m1+m2+m3) / 3

    def getRotation(self, m1, m2, m3):
        #https://math.stackexchange.com/questions/2249307/orientation-of-a-3d-plane-using-three-points
        N = np.cross((m1-m3),(m2-m3))
        U = N/ np.linalg.norm(N)
        rotations = np.arcsin(U)

        #transform to vpython rotation standard; normal vector (1,0,0)
        return np.matmul(self.rm4 , rotations)