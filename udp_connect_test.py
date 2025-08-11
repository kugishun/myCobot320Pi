# robot_receiver.py
import socket

LISTEN_IP = "0.0.0.0"  # 全インターフェースで受信
LISTEN_PORT = 7001     # PC送信側と合わせる

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening on {LISTEN_IP}:{LISTEN_PORT} ...")

while True:
    data, addr = sock.recvfrom(65535)
    print(f"Received from {addr}: {data.decode('utf-8')}")
