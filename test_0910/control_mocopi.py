import socket
import time
from pymycobot.mycobot320 import MyCobot320

# ====== myCobot接続 ======
mc = MyCobot320("/dev/ttyAMA0", 115200)
mc.power_on()

# 初期位置に移動（右腕を前に伸ばす想定）
init_pose = [90, 90, 0, -90, -90, 55]
mc.send_angles(init_pose, 30)
time.sleep(3)

# ====== UDP設定 ======
IP = "127.0.0.1"
PORT = 7001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print(f"[Python] Listening on {IP}:{PORT}")

# ====== 可動範囲 ======
JOINT_LIMITS = [
    (-165, 165),  # J1
    (-165, 165),  # J2
    (-165, 165),  # J3
    (-165, 165),  # J4
    (-165, 165),  # J5
    (-175, 175),  # J6
]

# ====== キャリブ用変数 ======
calib_euler = None

def map_angle(value, src_min, src_max, dst_min, dst_max):
    """範囲変換 & クリップ"""
    mapped = dst_min + (value - src_min) * (dst_max - dst_min) / (src_max - src_min)
    return max(min(mapped, dst_max), dst_min)

# ====== キャリブレーション ======
print("プログラム開始 → 2秒待機中...")
time.sleep(2)

print("5秒間、基準姿勢を保持してください（右腕を前に伸ばす）...")
samples = []
start_time = time.time()

while time.time() - start_time < 5.0:
    data, _ = sock.recvfrom(1024)
    msg = data.decode("utf-8").strip()
    try:
        x, y, z = [float(v) for v in msg.split(",")]
        samples.append((x, y, z))
    except:
        continue

if samples:
    calib_euler = (
        sum(s[0] for s in samples) / len(samples),
        sum(s[1] for s in samples) / len(samples),
        sum(s[2] for s in samples) / len(samples),
    )
    print("Calibration complete:", calib_euler)
else:
    print("Calibration failed: no data received.")
    exit(1)

# ====== 制御ループ ======
print("制御ループ開始！")
while True:
    data, _ = sock.recvfrom(1024)
    msg = data.decode("utf-8").strip()
    try:
        x, y, z = [float(v) for v in msg.split(",")]

        # 相対回転（基準との差分）
        dx = x - calib_euler[0]
        dy = y - calib_euler[1]
        dz = z - calib_euler[2]

        # J1〜J3へ割り当て（基準姿勢からの変化量として扱う）
        j1 = map_angle(dy, -90, 90, -60, 60)   # ベース回転
        j2 = map_angle(dx, -90, 90, -45, 45)   # 肩の上下
        j3 = map_angle(dz, -90, 90, -45, 45)   # 肘の曲げ

        # ロボット初期姿勢に加算
        angles = [
            init_pose[0] + j1,
            init_pose[1] + j2,
            init_pose[2] + j3,
            init_pose[3],  # 手首は固定
            init_pose[4],
            init_pose[5],
        ]

        # 可動範囲でクリップ
        angles = [
            max(min(a, JOINT_LIMITS[i][1]), JOINT_LIMITS[i][0])
            for i, a in enumerate(angles)
        ]

        print("send:", angles)
        mc.send_angles(angles, 30)

    except Exception as e:
        print("parse error:", msg, e)
