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
        self.rm1 = np.array(
                [[np.cos(np.pi), -np.sin(np.pi), 0],
                [np.sin(np.pi),   np.cos(np.pi), 0],
                [0., 0., 1.]]) @ \
                np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]])
            # 90deg y-axis -> -60deg z-axis
        self.rm2 = np.array(
                [[np.cos(-np.pi/3), -np.sin(-np.pi/3), 0],
                [np.sin(-np.pi/3),   np.cos(-np.pi/3), 0],
                [0., 0., 1.]]) @ \
                np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]])

            # 90deg y-axis -> 60deg z-axis
        self.rm3 = np.array(
                [[np.cos(np.pi/3), -np.sin(np.pi/3), 0],
                [np.sin(np.pi/3),   np.cos(np.pi/3), 0],
                [0., 0., 1.]]) @ \
                np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],
                [0,1,0],
                [-np.sin(np.pi/2),0,np.cos(np.pi/2)]])

    def solve(self, s1Input,s2Input,s3Input,multiplier=50000,normalize=True):
        if normalize:
            s1Input = self.normalizeInputData(s1Input,multiplier)
            s2Input = self.normalizeInputData(s2Input,multiplier)
            s3Input = self.normalizeInputData(s3Input,multiplier)

        v1 =  self.transformToRefrenceFrame(s1Input,self.rm1)
        v2 =  self.transformToRefrenceFrame(s2Input,self.rm2)
        v3 =  self.transformToRefrenceFrame(s3Input,self.rm3)

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

    def normalizeInputData(self, xyz, multiplier=50000) -> np.array:
        xyzPosNeg = np.absolute(xyz)/xyz
        xyz = 1/np.sqrt(np.absolute(xyz)) * xyzPosNeg * multiplier
        return xyz

    def transformToRefrenceFrame(self,xyz, transformMatrix) -> np.array:
        return transformMatrix @ xyz

    def getScaleFactor(self, sa, vsama, ma, sb, vsbmb, mb) -> np.array:
        factors = (-sa - (mb-ma) + sb) / (vsama-vsbmb)
        mask = np.isclose(factors,0)
        factors[mask] = np.nan
        return factors

    def getMeanScaleFactor(self, sf12,sf23,sf31) -> float:
        return np.nanmean(np.concatenate((sf12,sf23,sf31)))

    def getMagPosition(self, sensorPos, vector, sf) -> np.array:
        return sensorPos + vector * sf

    def getTranslation(self, m1, m2, m3) -> np.array:
        return  (m1+m2+m3) / 3

    def getRotation(self, m1, m2, m3) -> np.array:
        #https://math.stackexchange.com/questions/2249307/orientation-of-a-3d-plane-using-three-points
        N = np.cross((m1-m3),(m2-m3))
        U = N/ np.linalg.norm(N)
        return np.pi/2 - np.arccos(U)