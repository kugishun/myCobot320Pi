import socket
import json
from pymycobot.mycobot320 import MyCobot320

# myCobot接続
mc = MyCobot320("/dev/ttyAMA0", 115200)
mc.power_on()

# UDP受信設定
IP = "0.0.0.0"
PORT = 7010
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print(f"[myCobot Server] Listening on {IP}:{PORT}")

while True:
    data, _ = sock.recvfrom(1024)
    try:
        msg = json.loads(data.decode("utf-8"))
        angles = msg["angles"]
        print("[myCobot] recv:", angles)
        mc.send_angles(angles, 30)
    except Exception as e:
        print("parse error:", e)
