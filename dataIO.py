import socket
import time
from multiprocessing import Process, Value
import numpy as np

class dataIO:
    def __init__(self):
        #Listen to sensor information on port:
        UDP_PORT = 56200


    def getData(port):
        """
            Input:  socket connection of a sensor
            Output: Tuple with: side of robot, time of sending and 3x xyz numpy array of sensor values
        """
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.bind(('', port))

        data, _ = sock.recvfrom(255) # buffer size is 1024 bytes

        sock.close()
        data = data.decode('utf-8')
        row = data.split(';')

        side = row[0]
        time = row[1]
        s1Input = np.array([float(row[2]),float(row[3]),float(row[4])],dtype=np.float32)
        s2Input = np.array([float(row[5]),float(row[6]),float(row[7])],dtype=np.float32)
        s3Input = np.array([float(row[8]),float(row[9]),float(row[10])],dtype=np.float32)


        return((side,time,s1Input,s2Input,s3Input))



    def f(self, latestInput):
        latestInput = self.getData()

    if __name__ == '__main__':
        latestValue = ''

        p = Process(target=f, args=(latestValue))
        p.start()
        p.join()

        print(latestValue)