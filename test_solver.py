from socket import getservbyport
import unittest
import numpy as np
from solver import Solver

class TestModule(unittest.TestCase):
    # Test where all the sensor values indicate that the magnets is 10 units in the z axis
    # result should be that the inner ring is perfectly in the center
    def test_null(self):
        solver = Solver()

        s1Val = np.array([0,0,10])
        s2Val = np.array([0,0,10])
        s3Val = np.array([0,0,10])

        #skip data normalization

        vs1m1 = solver.transformToRefrenceFrame(s1Val,solver.rm1)
        vs2m2 = solver.transformToRefrenceFrame(s2Val,solver.rm2)
        vs3m3 = solver.transformToRefrenceFrame(s3Val,solver.rm3)

        np.testing.assert_array_almost_equal(vs1m1,np.array([-10,0,0]))
        np.testing.assert_array_almost_equal(vs2m2,np.array([5,-8.660254,0]))
        np.testing.assert_array_almost_equal(vs3m3,np.array([5, 8.660254,0]))

        sf12 = solver.getScaleFactor(solver.sp1,vs1m1,solver.mp1,solver.sp2,vs2m2,solver.mp2)
        sf23 = solver.getScaleFactor(solver.sp2,vs2m2,solver.mp2,solver.sp3,vs3m3,solver.mp3)
        sf31 = solver.getScaleFactor(solver.sp3,vs3m3,solver.mp3,solver.sp1,vs1m1,solver.mp1)

        np.testing.assert_array_almost_equal(sf12,np.array([1.28,1.28,np.nan]))
        np.testing.assert_array_almost_equal(sf23,np.array([np.nan,1.28,np.nan]))
        np.testing.assert_array_almost_equal(sf31,np.array([1.28,1.28,np.nan]))

        sf = solver.getMeanScaleFactor(sf12,sf23,sf31)
        self.assertAlmostEqual(sf,1.28)

        m1Pos = solver.getMagPosition(solver.sp1,vs1m1,sf)
        m2Pos = solver.getMagPosition(solver.sp2,vs2m2,sf)
        m3Pos = solver.getMagPosition(solver.sp3,vs3m3,sf)

        #Note this is only true in the case that the outer ring has no rotation or translation
        np.testing.assert_array_almost_equal(m1Pos,solver.mp1)
        np.testing.assert_array_almost_equal(m2Pos,solver.mp2)
        np.testing.assert_array_almost_equal(m3Pos,solver.mp3)

        outerPos = solver.getTranslation(m1Pos,m2Pos,m3Pos)

        np.testing.assert_array_almost_equal(outerPos,np.array([0,0,0]))

        outerRot = solver.getRotation(m1Pos,m2Pos,m3Pos)

    def test_singleTranslationInYDirection(self):
        solver = Solver()

        s1Val = np.array([0,-2.34375,10])
        s2Val = np.array([0,1.171875,7.97025296])
        s3Val = np.array([0,1.171875,12.0297470])

        vs1m1 = solver.transformToRefrenceFrame(s1Val,solver.rm1)
        vs2m2 = solver.transformToRefrenceFrame(s2Val,solver.rm2)
        vs3m3 = solver.transformToRefrenceFrame(s3Val,solver.rm3)

        np.testing.assert_array_almost_equal(vs1m1,np.array([-10,0        + 2.34375,0]))
        np.testing.assert_array_almost_equal(vs2m2,np.array([5,-8.660254  + 2.34375,0]))
        np.testing.assert_array_almost_equal(vs3m3,np.array([5, 8.660254  + 2.34375,0]))

        sf12 = solver.getScaleFactor(solver.sp1,vs1m1,solver.mp1,solver.sp2,vs2m2,solver.mp2)
        sf23 = solver.getScaleFactor(solver.sp2,vs2m2,solver.mp2,solver.sp3,vs3m3,solver.mp3)
        sf31 = solver.getScaleFactor(solver.sp3,vs3m3,solver.mp3,solver.sp1,vs1m1,solver.mp1)

        np.testing.assert_array_almost_equal(sf12,np.array([1.28,1.28,np.nan]))
        np.testing.assert_array_almost_equal(sf23,np.array([np.nan,1.28,np.nan]))
        np.testing.assert_array_almost_equal(sf31,np.array([1.28,1.28,np.nan]))

        sf = solver.getMeanScaleFactor(sf12,sf23,sf31)
        self.assertAlmostEqual(sf,1.28)

        m1Pos = solver.getMagPosition(solver.sp1,vs1m1,sf)
        m2Pos = solver.getMagPosition(solver.sp2,vs2m2,sf)
        m3Pos = solver.getMagPosition(solver.sp3,vs3m3,sf)

        np.testing.assert_array_almost_equal(m1Pos,np.array([-47, 0 + 3, 0]))
        np.testing.assert_array_almost_equal(m2Pos,np.array([23.5,-40.7031939 + 3,0]))
        np.testing.assert_array_almost_equal(m3Pos,np.array([23.5, 40.7031939 + 3,0]))

        outerPos = solver.getTranslation(m1Pos,m2Pos,m3Pos)

        np.testing.assert_array_almost_equal(outerPos,np.array([0,3,0]))

        outerRot = solver.getRotation(m1Pos,m2Pos,m3Pos)

    # def test_threeTranslations(self):

    #     #translated by (2,3,4) with scalingFactor 32