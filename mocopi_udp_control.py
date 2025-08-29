import socket, json, time, threading
from pymycobot.mycobot320 import MyCobot320

IP = "0.0.0.0"; PORT = 7010
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print(f"[robot] listening {IP}:{PORT}")

mc = MyCobot320("/dev/ttyAMA0", 115200)

latest_msg = None  # 最新データを保持する変数

def udp_listener():
    global latest_msg
    while True:
        data, addr = sock.recvfrom(65535)
        msg = json.loads(data.decode("utf-8"))
        latest_msg = msg  # 古い値は上書きされる

# 受信スレッド開始
threading.Thread(target=udp_listener, daemon=True).start()

# 制御ループ
while True:
    if latest_msg:
        msg = latest_msg
        x = float(msg["x"]); y = float(msg["y"]); z = float(msg["z"])
        rx = float(msg["rx"]); ry = float(msg["ry"]); rz = float(msg["rz"])
        speed = int(msg.get("speed", 30)); mode = int(msg.get("mode", 1))

        print(f"send_coords({x}, {y}, {z}, {rx}, {ry}, {rz})")
        mc.send_coords([x, y, z, rx, ry, rz], speed, mode)

    time.sleep(0.05)  # 20Hz（50ms周期）で更新
