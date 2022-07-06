import sys
sys.path.insert(0,'C:/Users/jorn-/Documents/school/y2/thesis/cuffling/code/Cuff_sensor/modules')
import time as t

from naoController import NaoController


nc = NaoController()
nc.setup()
nc.setStiffness(0.0)

while True:
    t.sleep(1.5)
    print(nc.getOrientation('LArm'))