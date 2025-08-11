# pi_udp_to_mycobot.py  （Raspberry Pi で実行）
import socket, json, time
from pymycobot.mycobot320 import MyCobot320

IP = "0.0.0.0"; PORT = 7010
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print(f"[robot] listening {IP}:{PORT}")

# 例：/dev/ttyAMA0 や /dev/ttyUSB0 等、Piの接続に合わせて
mc = MyCobot320("/dev/ttyAMA0", 115200)
# mc.power_on()
# mc.init_eletric_gripper()  # 機種により

last_ts = time.time()
while True:
    data, addr = sock.recvfrom(65535)
    msg = json.loads(data.decode("utf-8"))

    x = float(msg["x"]); y = float(msg["y"]); z = float(msg["z"])
    rx = float(msg["rx"]); ry = float(msg["ry"]); rz = float(msg["rz"])
    speed = int(msg.get("speed", 30))
    mode  = int(msg.get("mode", 1))

    # ウォッチドッグ（任意）：受信間隔が空いたら何か処理するなど
    last_ts = time.time()

    # 実行
    mc.send_coords([x, y, z, rx, ry, rz], speed, mode)
