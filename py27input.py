import socket               # Import socket module
from leftArmController import LeftArmController
import time

sf = 10

controller = LeftArmController()
controller.setup()

s = socket.socket()         # Create a socket object
s.bind(('0.0.0.0', 5678))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   if c:
        while True:
            rawdata =  c.recv(1024)
            decoded = rawdata.decode('utf-8')

            print(decoded)
            xyz = decoded.split('x')[0].split(';')
            print(xyz)
            xyz[0] = float(xyz[0]) /1000/ sf
            xyz[1] = float(xyz[1]) /1000/ sf
            xyz[2] = float(xyz[2]) /1000 / sf

            controller.relativeMove(xyz)
            time.sleep(.5/sf)
 