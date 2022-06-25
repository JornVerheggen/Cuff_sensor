import socket
from solver import Solver
import numpy as np 
import keyboard
import statistics
import time

solver = Solver()
UDP_PORT = 56201

while True:
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.bind(('', UDP_PORT))


    time.sleep(1)
    for i in range(20):
        sensor1Result = []
        sensor2Result = []
        sensor3Result = []

        data, addr = sock.recvfrom(255) # buffer size is 1024 bytes
        data = data.decode('utf-8')
        row = data.split(';')

        s1Input = np.array([float(row[2]),float(row[3]),float(row[4])],dtype=np.float32)
        s2Input = np.array([float(row[5]),float(row[6]),float(row[7])],dtype=np.float32)
        s3Input = np.array([float(row[8]),float(row[9]),float(row[10])],dtype=np.float32)

        trans,aAngle,magPositions = solver.solve( s1Input,
                                                    s2Input,
                                                    s3Input,
                                                    normalize= False, 
                                                    visualisationData = True)

        sensor1Result.append(magPositions[0][0])
        sensor2Result.append(magPositions[1][0])
        sensor3Result.append(magPositions[2][0])
    
    print('\n')
    print(f"s1: {statistics.mean(sensor1Result):.3f}".replace('.',','))
    print(f"s2: {statistics.mean(sensor2Result):.3f}".replace('.',','))
    print(f"s3: {statistics.mean(sensor3Result):.3f}".replace('.',','))

    while True:
        if keyboard.is_pressed("space"):
            sock.close()
            break
        time.sleep(.2)