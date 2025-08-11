# recv_to_mycobot_min.py
import socket, json, math
from pymycobot.mycobot320 import MyCobot320

UDP_IP = "0.0.0.0"; UDP_PORT = 7001

# ---- キャリブ（最初は仮でOK） ----
# Unity→Robot の並進 [mm]（作業原点・設置位置に合わせて後で調整）
T_U2R = [200.0, 0.0, 250.0]

def clip(v, lo, hi): return max(lo, min(hi, v))

# ---- Robot 接続 ----
# 例: Windowsなら "COM3" 等。あなたのポート名に変更
mc = MyCobot320("/dev/ttyAMA0", 115200)
# mc.power_on()

# ---- UDP 待受 ----
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"listening on {UDP_IP}:{UDP_PORT}")
mc.send_angles([0, 0, 0, 0, 0, 0], 50)

while True:
    data, addr = sock.recvfrom(65535)
    m = json.loads(data.decode("utf-8"))
    pos = m["pos"]; eul = m["eul"]

    # m→mm + 並進オフセット（最初はZだけ上げるなどでOK）
    x = pos["x"]*1000.0 + T_U2R[0]
    y = pos["y"]*1000.0 + T_U2R[1]
    z = pos["z"]*1000.0 + T_U2R[2]

    rx = eul["rx"]  # deg
    ry = eul["ry"]
    rz = eul["rz"]

    # 最低限の安全クリップ（必要に応じて調整）
    z = clip(z, 150.0, 400.0)

    # 送信（内部IKに任せる）
    mc.send_coords([x, y, z, rx, ry, rz], 30, 1)  # speed=30, 直線補間 mode=1
