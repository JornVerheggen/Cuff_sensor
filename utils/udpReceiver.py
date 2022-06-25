import socket

UDP_PORT = 56201

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

while True:
    data, addr = sock.recvfrom(255)
    print(f"received message: {data.decode('utf-8')}")

