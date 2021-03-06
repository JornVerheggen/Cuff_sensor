import sys
sys.path.insert(0,'C:/Users/jorn-/Documents/school/y2/thesis/cuffling/code/Cuff_sensor/modules')
import socket
from visualize import Viz
from solver import Solver
import numpy as np 

vis = Viz()
solver = Solver()

UDP_PORT = 56201

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

while True:
    data, addr = sock.recvfrom(255)
    data = data.decode('utf-8')
    row = data.split(';')

    s1Input = np.array([float(row[2]),float(row[3]),float(row[4])],dtype=np.float32)
    s2Input = np.array([float(row[5]),float(row[6]),float(row[7])],dtype=np.float32)
    s3Input = np.array([float(row[8]),float(row[9]),float(row[10])],dtype=np.float32)

    homTrans, trans,aAngle,magPositions = solver.solve( s1Input,
                                                s2Input,
                                                s3Input,
                                                normalize= False, 
                                                visualisationData = True)

    vis.setPosition(trans)
    vis.setRotation(aAngle)
    vis.setMagPositions(magPositions)
    vis.setHandPointer(homTrans)

    # if np.all(solver.offset) == np.all(np.array([0.0,0.0,0.0])):
    #     solver.setOffset(s1Input,s2Input,s3Input)