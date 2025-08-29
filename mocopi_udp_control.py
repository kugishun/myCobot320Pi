# bridge_mocopi_to_mycobot.py
# mocopi(肩基準) → キャリブ → ロボット追従 (位置+回転)

import socket, json, time, math, numpy as np
from pymycobot.mycobot320 import MyCobot320

# ===== 1) 設定 =====
IN_IP, IN_PORT = "0.0.0.0", 7001   # mocopi UDP
mc = MyCobot320("/dev/ttyAMA0", 115200)  # myCobot接続

CALIB_SEC = 5.0
SEND_SPEED = 30
SEND_MODE  = 1

# Unity→Robot 軸変換
M = np.array([[-1,0,0],
              [ 0,0,-1],
              [ 0,1, 0]], float)

# 人間とロボットの腕長比でスケーリング
human_arm_len = 0.60   # 人間の肩〜手首[m] (実測値で調整してください)
robot_arm_len = 0.32   # myCobot320の最大リーチ[m]
scale = robot_arm_len / human_arm_len

# ===== 2) ユーティリティ =====
def wrap180(a): return (a+180)%360-180

def euler_xyz_deg_to_R(rx, ry, rz):
    ax, ay, az = map(math.radians, (rx, ry, rz))
    cx, sx = math.cos(ax), math.sin(ax)
    cy, sy = math.cos(ay), math.sin(ay)
    cz, sz = math.cos(az), math.sin(az)
    Rx = np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
    Ry = np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
    Rz = np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
    return Rz @ Ry @ Rx

def euler_xyz_intrinsic_from_R(R):
    sy = -R[2,0]
    sy = max(-1.0, min(1.0, sy))
    cy = math.sqrt(max(0.0, 1.0 - sy*sy))
    if cy > 1e-8:
        roll  = math.degrees(math.atan2(R[2,1], R[2,2]))
        pitch = math.degrees(math.asin(sy))
        yaw   = math.degrees(math.atan2(R[1,0], R[0,0]))
    else:
        roll  = math.degrees(math.atan2(-R[1,2], R[1,1]))
        pitch = math.degrees(math.asin(sy))
        yaw   = 0.0
    return np.array([roll, pitch, yaw], float)

# myCobot規約: order=XYZ, intrinsic, sgn=(+1,-1,-1), off=[-90,-0.5,-178]
def mycobot_euler_from_R(R):
    rpy = euler_xyz_intrinsic_from_R(R)
    rx =  +1 * rpy[0] + (-90.0)
    ry =  -1 * rpy[1] + (-0.5)
    rz =  -1 * rpy[2] + (-178.0)
    return np.array([wrap180(rx), wrap180(ry), wrap180(rz)], float)

# ===== 3) ソケット =====
sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_in.bind((IN_IP, IN_PORT))

print(f"[bridge] listening {IN_IP}:{IN_PORT}")
time.sleep(2)

# ===== 4) キャリブレーション =====
print(f"[calib] 肩基準で腕を前に伸ばしたまま {CALIB_SEC} 秒...")
pos_buf, eul_buf = [], []
t0 = time.time()
while time.time()-t0 < CALIB_SEC:
    data,_ = sock_in.recvfrom(65535)
    msg = json.loads(data.decode("utf-8"))
    p = msg["pos_rel"]
    r = msg["eul_rel"]
    pos_buf.append([float(p["x"]), float(p["y"]), float(p["z"])])
    eul_buf.append([float(r["rx"]), float(r["ry"]), float(r["rz"])])
p0_human = np.mean(np.array(pos_buf), axis=0)  # [m]
R0_human = euler_xyz_deg_to_R(*np.mean(np.array(eul_buf), axis=0))

coords0 = mc.get_coords()
p0_robot = np.array(coords0[0:3], float)       # [mm]
R0_robot = euler_xyz_deg_to_R(*coords0[3:6])

print("[calib] 完了。追従開始。Ctrl+Cで終了。")

# ===== 5) 追従ループ =====
while True:
    data,_ = sock_in.recvfrom(65535)
    msg = json.loads(data.decode("utf-8"))
    p_h = np.array([msg["pos_rel"]["x"], msg["pos_rel"]["y"], msg["pos_rel"]["z"]], float) # [m]
    r_h = np.array([msg["eul_rel"]["rx"], msg["eul_rel"]["ry"], msg["eul_rel"]["rz"]], float)
    R_h = euler_xyz_deg_to_R(*r_h)

    # 相対
    dp_h = p_h - p0_human
    R_rel_h = R_h @ R0_human.T

    # mocopi→robot変換
    dp_r = scale * (M @ (dp_h*1000.0))   # [mm]
    p_cmd = p0_robot + dp_r

    R_rel_r = M @ R_rel_h @ M.T
    R_cmd   = R_rel_r @ R0_robot
    e_cmd   = mycobot_euler_from_R(R_cmd)

    mc.send_coords([p_cmd[0], p_cmd[1], p_cmd[2],
                    e_cmd[0], e_cmd[1], e_cmd[2]],
                   SEND_SPEED, SEND_MODE)
