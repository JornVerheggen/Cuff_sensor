from rotMat import getRotmat3

import numpy as np
import rmsd

class Solver:

    def __init__(self):
        #define sensor positions
        self.sp1 = np.array([0.,-0.0342, 0.])
        self.sp2 = np.array([0., 0.0171,-0.0296180688])
        self.sp3 = np.array([0., 0.0171, 0.0296180688])
    
        #define magnet positions without any rotation/translation
        self.mp1 = np.array([0.,-0.047, .0])
        self.mp2 = np.array([0.,0.0235, -0.0407031939])
        self.mp3 = np.array([0.,0.0235, 0.0407031939])

        #define sensor rotation matrices
        # self.rm1 = np.matmul(getRotmat3('x',np.pi/2),getRotmat3('z',np.pi))
        # self.rm2 = np.matmul(getRotmat3('x',-5*np.pi/6),getRotmat3('z',np.pi))
        # self.rm3 = np.matmul(getRotmat3('x',np.pi/6),getRotmat3('z',np.pi))
        
        self.rm1 = getRotmat3('x',np.pi/2)
        self.rm2 = getRotmat3('x',-5*np.pi/6)
        self.rm3 = getRotmat3('x',np.pi/6)

        self.offCenterMat = np.matmul(getRotmat3('y',.1),getRotmat3('x',.2))
        self.ocsp1 = np.matmul(self.offCenterMat,self.sp1)
        self.ocsp2 = np.matmul(self.offCenterMat,self.sp2)
        self.ocsp3 = np.matmul(self.offCenterMat,self.sp3)

        self.ocmp1 = np.matmul(self.offCenterMat,self.mp1)
        self.ocmp2 = np.matmul(self.offCenterMat,self.mp2)
        self.ocmp3 = np.matmul(self.offCenterMat,self.mp3)


        #Offset variables
        self.offset = np.array([0.0,0.0,0.0])

    def solve(      self, 
                    s1Input,
                    s2Input,
                    s3Input,
                    normalize=True, 
                    visualisationData = False, 
                ):
        """
        Takes the raw sensor values and calculates the difference between the outer ring and inner ring
        input:  s1Input, s2Input, s3Input: np.array of shape (3,)
                normalize, returnPosition, returnAxisAngle, returnMagnetPositions booleans
        output: Homogeneous transform of outer ring with reference frame inner ring
        """

        if normalize:
            #Invert the z-axis so that value increases as magnet goes farther away from the sensor
            s1NormInput = s1Input * -1
            s2NormInput = s2Input * -1
            s3NormInput = s3Input * -1
        else: 
            s1NormInput = s1Input            
            s2NormInput = s2Input            
            s3NormInput = s3Input

        v1 =  self.transformToRefrenceFrame(s1NormInput,self.rm1)
        v2 =  self.transformToRefrenceFrame(s2NormInput,self.rm2)
        v3 =  self.transformToRefrenceFrame(s3NormInput,self.rm3)

        ocv1 = np.matmul(self.offCenterMat,v1)
        ocv2 = np.matmul(self.offCenterMat,v2)
        ocv3 = np.matmul(self.offCenterMat,v3)

        sf12 = np.absolute(self.getScaleFactor(self.ocsp1,ocv1,self.ocmp1,self.ocsp2,ocv2,self.ocmp2))
        sf23 = np.absolute(self.getScaleFactor(self.ocsp2,ocv2,self.ocmp2,self.ocsp3,ocv3,self.ocmp3))
        sf31 = np.absolute(self.getScaleFactor(self.ocsp3,ocv3,self.ocmp3,self.ocsp1,ocv1,self.ocmp1))

        sf = self.getMeanScaleFactor(sf12,sf23,sf31)

        m1Pos = self.getMagPosition(self.sp1,v1,sf)
        m2Pos = self.getMagPosition(self.sp2,v2,sf)
        m3Pos = self.getMagPosition(self.sp3,v3,sf)

        #Include offset
        m1Pos = m1Pos + self.offset
        m2Pos = m2Pos + self.offset
        m3Pos = m3Pos + self.offset

        #Set a soft maximum of +/- 25mm for outliers
        m1Pos = 0.025*np.tanh(m1Pos/0.025)
        m2Pos = 0.025*np.tanh(m2Pos/0.025)
        m3Pos = 0.025*np.tanh(m3Pos/0.025)

        outerTrans = self.getTranslation(m1Pos,m2Pos,m3Pos)
        outerRot = self.getRotation(m1Pos,m2Pos,m3Pos)

        if visualisationData:
            return (self.getHomogeneousTransform(outerTrans, outerRot),outerTrans,self.getAxisAngle(outerRot),[m1Pos,m2Pos,m3Pos])

        return self.getHomogeneousTransform(outerTrans, outerRot)
    
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
        a = np.stack([self.mp1,self.mp2,self.mp3])
        b = np.stack([m1,m2,m3])

        R = rmsd.kabsch(a, b)
        return R
    
    def getAxisAngle(self,rotation):
        return np.matmul(np.array([1,0,0]),rotation)
    
    def getHomogeneousTransform(self, translation, rotation):
        homTrans = np.identity(4)
        homTrans[:3,:3] = rotation
        homTrans[:3,3] = translation
        return homTrans

    def setOffset(  self, 
                    s1Input,
                    s2Input,
                    s3Input):
        _,_,_, offsets = self.solve(s1Input,s2Input,s3Input,visualisationData = True)
        self.offset = (offsets[0] + offsets[1] + offsets[2])/3
        print("Offset created: "+str(self.offset))
        
