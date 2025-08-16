# pi_udp_to_mycobot.py  （Raspberry Pi で実行）
import socket, json, time
from pymycobot.mycobot320 import MyCobot320

IP = "0.0.0.0"; PORT = 7010
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print(f"[robot] listening {IP}:{PORT}")

# 例：/dev/ttyAMA0 や /dev/ttyUSB0 等、Piの接続に合わせて
mc = MyCobot320("/dev/ttyAMA0", 115200)
max_angle = {
    "x": (-350.0, 350.0),
    "y": (-350.0, 350.0),
    "z": (165.0, 523.9)
} 
# mc.power_on()
# mc.init_eletric_gripper()  # 機種により
mc.send_angles([-18, 85, 3, 24.5, 0, 96], 40)
time.sleep(3)
mc.send_angles([0, 0, 0, 0, 0, 0], 50,1)

last_ts = time.time()
print("while start")
while True:
    print("While 1")
    data, addr = sock.recvfrom(65535)
    print("sock.recvfrom Done")
    msg = json.loads(data.decode("utf-8"))
    # print(f"msg: {msg}")

    if max_angle["x"][1]<float(msg["x"]):
        x = max_angle["x"][1]
    elif max_angle["x"][0]>float(msg["x"]):
        x = max_angle["x"][0]
    else:
        x = float(msg["x"])

    if max_angle["y"][1]<float(msg["y"]):
        y = max_angle["y"][1]
    elif max_angle["y"][0]>float(msg["y"]):
        y = max_angle["y"][0]
    else:
        y = float(msg["y"])

    if max_angle["z"][1]<float(msg["z"]):
        z = max_angle["z"][1]
    elif max_angle["z"][0]>float(msg["z"]):
        z = max_angle["z"][0]
    else:
        z = float(msg["z"])

    rx = float(msg["rx"]); ry = float(msg["ry"]); rz = float(msg["rz"])
    speed = int(msg.get("speed", 30))
    mode  = int(msg.get("mode", 1))

    # ウォッチドッグ（任意）：受信間隔が空いたら何か処理するなど
    last_ts = time.time()
    print(f"send_angles[{x},{y},{z},{rx},{ry},{rz}]")
    # 実行
    mc.send_coords([x, y, z, rx, ry, rz], speed, mode)
    mc.send_angle(6,50,50)
    time.sleep(0.1)
