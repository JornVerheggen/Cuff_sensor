from socket import getservbyport
import unittest
import numpy as np
from solver import normalizeInputData, transformToRefrenceFrame, getScale, getMagPosition, getTransrot, getTransmat, getMp, getSp

class TestModule(unittest.TestCase):
    # Test where all the sensor values indicate that the magnets is 10 units in the z axis
    # result should be that the inner ring is perfectly in the center
    def test_null(self):
        s1Val = np.array([0,0,10])
        s2Val = np.array([0,0,10])
        s3Val = np.array([0,0,10])

        #skip data normalization

        vs1m1 = transformToRefrenceFrame(s1Val,getTransmat(1))
        vs2m2 = transformToRefrenceFrame(s2Val,getTransmat(2))
        vs3m3 = transformToRefrenceFrame(s3Val,getTransmat(3))

        print(vs1m1)
        np.testing.assert_array_almost_equal(vs1m1,np.array([-10,0,0]))
        np.testing.assert_array_almost_equal(vs2m2,np.array([8.660,-5,0]))
        np.testing.assert_array_almost_equal(vs3m3,np.array([8.660,5,0]))

        sf12 = getScale(getSp(1),vs1m1,getMp(1),getSp(2),vs2m2,getMp(2))

        print("sf12 moet volgens mij zijn: 1.28")
