from modules.naoController import NaoController
from modules.keyBoardHandler import KeyboardHandler
import numpy as np 

if __name__ == '__main__':
    nc = NaoController(robotIP='192.168.0.121') #Create naoController object
    kbh = KeyboardHandler() #Create  KeyboardHandler object

    #move robot arm to front to start moving
    nc.setup()

    while(True):
        homTrans = kbh.getSingleTransform()
        nc.moveTo(np.matmul(nc.getOrientation('LArm'),homTrans))