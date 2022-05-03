import socket

UDP_IP = "192.168.1.21"
UDP_PORT = 56200

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

while True:
    data, addr = sock.recvfrom(255)
    print(f"received message: {data.decode('utf-8')}" )