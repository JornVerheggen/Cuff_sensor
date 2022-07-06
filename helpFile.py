import numpy as np 
import sys
from modules.solver import Solver
from modules.naoController import NaoController
from modules.dataIO import DataIO
from modules.rotMat import getEuler3, getRotmat3, getRotmat4, getEuler4
import time as t
import math


nc = NaoController()

nc.setStiffness(0.0)

while True:
    torso2Hand = nc.getOrientation('LArm')

    print(getEuler4(torso2Hand))

    t.sleep(1)
