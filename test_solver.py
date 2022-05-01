from socket import getservbyport
import unittest
import numpy as np
from solver import normalizeInputData, transformToRefrenceFrame, getScaleFactor, getMeanScaleFactor, getMagPosition, getTranslation, getRotation, getRotMat, getMp, getSp

class TestModule(unittest.TestCase):
    # Test where all the sensor values indicate that the magnets is 10 units in the z axis
    # result should be that the inner ring is perfectly in the center
    def test_null(self):
        s1Val = np.array([0,0,10])
        s2Val = np.array([0,0,10])
        s3Val = np.array([0,0,10])

        #skip data normalization

        vs1m1 = transformToRefrenceFrame(s1Val,getRotMat(1))
        vs2m2 = transformToRefrenceFrame(s2Val,getRotMat(2))
        vs3m3 = transformToRefrenceFrame(s3Val,getRotMat(3))

        np.testing.assert_array_almost_equal(vs1m1,np.array([-10,0,0]))
        np.testing.assert_array_almost_equal(vs2m2,np.array([5,-8.660254,0]))
        np.testing.assert_array_almost_equal(vs3m3,np.array([5, 8.660254,0]))

        sf12 = getScaleFactor(getSp(1),vs1m1,getMp(1),getSp(2),vs2m2,getMp(2))
        sf23 = getScaleFactor(getSp(2),vs2m2,getMp(2),getSp(3),vs3m3,getMp(3))
        sf31 = getScaleFactor(getSp(3),vs3m3,getMp(3),getSp(1),vs1m1,getMp(1))

        np.testing.assert_array_almost_equal(sf12,np.array([1.28,1.28,np.nan]))
        np.testing.assert_array_almost_equal(sf23,np.array([np.nan,1.28,np.nan]))
        np.testing.assert_array_almost_equal(sf31,np.array([1.28,1.28,np.nan]))

        sf = getMeanScaleFactor(sf12,sf23,sf31)
        self.assertAlmostEqual(sf,1.28)

        m1Pos = getMagPosition(getSp(1),vs1m1,sf)
        m2Pos = getMagPosition(getSp(2),vs2m2,sf)
        m3Pos = getMagPosition(getSp(3),vs3m3,sf)

        #Note this is only true in the case that the outer ring has no rotation or translation
        np.testing.assert_array_almost_equal(m1Pos,getMp(1))
        np.testing.assert_array_almost_equal(m2Pos,getMp(2))
        np.testing.assert_array_almost_equal(m3Pos,getMp(3))

        outerPos = getTranslation(m1Pos,m2Pos,m3Pos)

        np.testing.assert_array_almost_equal(outerPos,np.array([0,0,0]))

        outerRot = getRotation(m1Pos,m2Pos,m3Pos)
        print(outerRot)



