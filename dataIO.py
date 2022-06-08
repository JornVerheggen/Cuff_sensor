import time
from multiprocessing import Process, Queue
import numpy as np
import socket
import os

class dataIO:
    """
    Creates a seperate thread that continiously gets the latest sensor values and stores them in shared memory
    """
    def __init__(self,port = 56200):
        self.UDP_PORT = port
        self.queue = Queue()
        self.lastItem = None

    def startProcess(self):
        self.p = Process(target=self.thread,args=(self.queue,'x')) #x because of bug in multiprocessing module
        self.p.start()

    def getRawData(self):
        while not self.queue.empty():
            self.lastItem = self.queue.get()

    def getFormattedData(self):
        self.getRawData()
        if self.lastItem == None:
            while self.lastItem == None: #ensures data is present
                self.getRawData()
                time.sleep(.5)
                print("waiting for first data packet..")
                print(self.lastItem)

        row = self.lastItem.split(';')
        side = row[0]
        timeOfSending = row[1]
        s1Input = np.array([float(row[2]),float(row[3]),float(row[4])],dtype=np.float32)
        s2Input = np.array([float(row[5]),float(row[6]),float(row[7])],dtype=np.float32)
        s3Input = np.array([float(row[8]),float(row[9]),float(row[10])],dtype=np.float32)

        return((side,timeOfSending,s1Input,s2Input,s3Input))

    def thread(self,queue,_):
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
            sock.bind(('', self.UDP_PORT))

            while True:
                data, _ = sock.recvfrom(255)
                queue.put(str(data.decode('utf-8')))