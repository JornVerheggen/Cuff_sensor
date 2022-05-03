import socket
import visualize as vis
from solver import Solver
import numpy as np 

import random as r


vis.init()

solver = Solver()

UDP_IP = "192.168.1.21"
UDP_PORT = 5620

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

while True:
    data, addr = sock.recvfrom(255) # buffer size is 1024 bytes
    data = data.decode('utf-8')
    row = data.split(';')

    s1Input = np.array([float(row[2]),float(row[3]),float(row[4])],dtype=np.float16)
    s2Input = np.array([float(row[5]),float(row[6]),float(row[7])],dtype=np.float16)
    s3Input = np.array([float(row[8]),float(row[9]),float(row[10])],dtype=np.float16)

    trans, rot = solver.solve(s1Input,s2Input,s3Input,multiplier=10000,normalize= False)

    vis.setPosition(trans)
    #vis.setRotation(rot)
