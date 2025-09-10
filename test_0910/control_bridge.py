import socket
import json
import threading
import queue
import time
from pymycobot.mycobot320 import MyCobot320

# ====== myCobot接続 ======
mc = MyCobot320("/dev/ttyAMA0", 115200)
mc.power_on()

# ====== UDP設定 ======
IP = "0.0.0.0"
PORT = 7010
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print(f"[myCobot Server] Listening on {IP}:{PORT}")

# ====== 共有キュー ======
angle_queue = queue.Queue()

# ====== UDP受信スレッド ======
def udp_receiver():
    while True:
        data, _ = sock.recvfrom(1024)
        try:
            msg = json.loads(data.decode("utf-8"))
            angles = msg["angles"]
            angle_queue.put(angles)  # キューに格納
        except Exception as e:
            print("parse error:", e)

# ====== 制御スレッド ======
def arm_controller():
    last_angles = None
    while True:
        try:
            # 最新データを取得（古いものは破棄）
            while not angle_queue.empty():
                last_angles = angle_queue.get_nowait()

            if last_angles is not None:
                print("[myCobot] recv:", last_angles)
                mc.send_angles(last_angles, 30)

            time.sleep(0.05)  # 20Hz更新
        except Exception as e:
            print("control error:", e)

# ====== スレッド起動 ======
t1 = threading.Thread(target=udp_receiver, daemon=True)
t2 = threading.Thread(target=arm_controller, daemon=True)

t1.start()
t2.start()

# メインスレッドを待機状態にする
while True:
    time.sleep(1)
