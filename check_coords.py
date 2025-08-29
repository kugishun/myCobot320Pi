import csv, time
from pymycobot import MyCobot320

# === 接続設定 ===
mc = MyCobot320("/dev/ttyAMA0", 115200)

# === 記録する姿勢リスト ===
# 各要素は [j1,j2,j3,j4,j5,j6] (角度deg)
pose_list = [
    [0,0,0,0,0,0],       # ゼロ姿勢
    [30,0,0,0,0,0],      # J1 +30
    [-30,0,0,0,0,0],     # J1 -30
    [0,30,0,0,0,0],      # J2 +30
    [0,-30,0,0,0,0],     # J2 -30
    [0,0,30,0,0,0],      # J3 +30
    [0,0,-30,0,0,0],     # J3 -30
    [0,0,0,30,0,0],      # J4 +30
    [0,0,0,-30,0,0],     # J4 -30
    [0,0,0,0,30,0],      # J5 +30
    [0,0,0,0,90,0],      # J5 +90
    [0,0,0,0,-30,0],     # J5 -30
    [0,0,0,0,-90,0],     # J5 -90
    [0,0,0,0,0,30],      # J6 +30
    [0,0,0,0,0,-30],     # J6 -30
]

# === 出力ファイル ===
out_file = "mycobot_coords_log.csv"

with open(out_file, "w", newline="") as f:
    writer = csv.writer(f)
    # ヘッダ
    writer.writerow(["j1","j2","j3","j4","j5","j6",
                     "x","y","z","rx","ry","rz"])
    
    # 姿勢ごとに記録
    for pose in pose_list:
        print(f"Moving to {pose} ...")
        mc.send_angles(pose, 20)   # speed=20
        time.sleep(3)              # 移動完了待ち

        coords = mc.get_coords()   # [x,y,z,rx,ry,rz]
        print(" -> coords:", coords)
        row = pose + coords
        writer.writerow(row)

print(f"\nログを {out_file} に保存しました！")
