import socket
import visualize as vis
from solver import Solver
import numpy as np 

vis.init()
solver = Solver()

UDP_PORT = 56201

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

with socket.socket() as s: 
    s.connect(('localhost', 5678))

    while True:
        data, addr = sock.recvfrom(255) # buffer size is 1024 bytes
        data = data.decode('utf-8')
        row = data.split(';')

        s1Input = np.array([float(row[2]),float(row[3]),float(row[4])],dtype=np.float32)
        s2Input = np.array([float(row[5]),float(row[6]),float(row[7])],dtype=np.float32)
        s3Input = np.array([float(row[8]),float(row[9]),float(row[10])],dtype=np.float32)

        trans, rot = solver.solve(s1Input,s2Input,s3Input,normalize= True)

        vis.setPosition(trans)
        vis.setRotation(rot)

        message = ';'.join([str(i) for i in trans])

        message += 'x'

        # Create a socket object
        print(f"sending: {message}")

        s.sendall(message.encode('utf-8'))