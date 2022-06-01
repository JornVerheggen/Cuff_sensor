import sys
sys.path.insert(0, '../')
from naoController import naoController

naoController = naoController() #Create naoController object

naoController.rest()

