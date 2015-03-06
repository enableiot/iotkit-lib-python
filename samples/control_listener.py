import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 41235

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
print "Listening on port", UDP_PORT

while True:
    data, addr = sock.recvfrom(4096)  # buffer size is 1024 bytes
    print "received message:", data
