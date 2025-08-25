import numpy as np
import math

# --- 基本的なDH行列を作る関数 ---
def dh_matrix(a, alpha, d, theta):
    ca, sa = math.cos(math.radians(alpha)), math.sin(math.radians(alpha))
    ct, st = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,      sa,     ca,    d],
        [0,       0,      0,    1]
    ], dtype=float)

# --- myCobot320のDHパラメータ ---
DH_PARAMS = [
    (0,     90, 131.56),   # J1
    (-110,   0,   0),      # J2
    (-96,    0,   0),      # J3
    (0,     90, 131.25),   # J4
    (0,    -90,  96),      # J5
    (0,      0, 156.4)     # J6
]

# --- FK計算 ---
def forward_kinematics(joints):
    T = np.eye(4)
    for (a, alpha, d), theta in zip(DH_PARAMS, joints):
        T = T @ dh_matrix(a, alpha, d, theta)
    return T

# --- 回転行列からオイラー角変換（任意の順序） ---
def rot_to_euler(R, order="ZYX"):
    if order == "ZYX":  # Yaw-Pitch-Roll
        sy = math.sqrt(R[0,0]**2 + R[1,0]**2)
        if sy > 1e-6:
            x = math.degrees(math.atan2(R[2,1], R[2,2]))
            y = math.degrees(math.atan2(-R[2,0], sy))
            z = math.degrees(math.atan2(R[1,0], R[0,0]))
        else:
            x = math.degrees(math.atan2(-R[1,2], R[1,1]))
            y = math.degrees(math.atan2(-R[2,0], sy))
            z = 0
        return [x,y,z]

    elif order == "XYZ":  # Roll-Pitch-Yaw
        sy = -R[2,0]
        cy = math.sqrt(1 - sy**2)
        if cy > 1e-6:
            x = math.degrees(math.atan2(R[2,1], R[2,2]))
            y = math.degrees(math.asin(sy))
            z = math.degrees(math.atan2(R[1,0], R[0,0]))
        else:
            x = math.degrees(math.atan2(-R[1,2], R[1,1]))
            y = math.degrees(math.asin(sy))
            z = 0
        return [x,y,z]
    
    # 必要なら ZYZ なども実装可
    else:
        raise NotImplementedError("未対応の順序")

# --- テスト ---
joints = [0,0,0,0,0,0]   # 全ジョイント0度
T = forward_kinematics(joints)
R = T[:3,:3]

print("回転行列 R =\n", R)
print("Euler ZYX:", rot_to_euler(R, "ZYX"))
print("Euler XYZ:", rot_to_euler(R, "XYZ"))
