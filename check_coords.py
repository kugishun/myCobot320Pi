import csv, time
from pymycobot import MyCobot320

# === 接続 ===
mc = MyCobot320("/dev/ttyAMA0", 115200)

# === 記録する姿勢リスト ===
pose_list = [
    # 単軸 (基本)
    [0,0,0,0,0,0],
    [30,0,0,0,0,0], [-30,0,0,0,0,0],
    [0,30,0,0,0,0], [0,-30,0,0,0,0],
    [0,0,30,0,0,0], [0,0,-30,0,0,0],
    [0,0,0,30,0,0], [0,0,0,-30,0,0],
    [0,0,0,0,30,0], [0,0,0,0,-30,0],
    [0,0,0,0,90,0], [0,0,0,0,-90,0],
    [0,0,0,0,0,30], [0,0,0,0,0,-30],

    # --- 複合ポーズ ---
    [30,30,0,0,0,0],   # J1+J2
    [-30,30,0,0,0,0],  # J1-30 & J2+30
    [30,0,30,0,0,0],   # J1+J3
    [0,30,0,30,0,0],   # J2+J4
    [0,0,30,0,30,0],   # J3+J5
    [0,0,0,30,30,0],   # J4+J5
    [30,30,30,0,0,0],  # J1+J2+J3
    [0,30,-30,30,0,0], # J2+J3+J4 複合
    [0,60,-60,0,0,0],  # 大きめ: J2+J3
    [0,0,0,0,120,0],   # J5 +120
    [0,0,0,0,-120,0],  # J5 -120
]

# === 出力ファイル ===
out_file = "mycobot_coords_log_complex.csv"

with open(out_file, "w", newline="") as f:
    writer = csv.writer(f)
    # ヘッダ
    writer.writerow(["j1","j2","j3","j4","j5","j6",
                     "x","y","z","rx","ry","rz"])
    
    # 記録ループ
    for pose in pose_list:
        print(f"Moving to {pose} ...")
        mc.send_angles(pose, 50)   # speed=20
        time.sleep(3)              # 移動完了待ち（余裕を持って4秒）
        
        coords = mc.get_coords()   # [x,y,z,rx,ry,rz]
        print(" -> coords:", coords)
        row = pose + coords
        writer.writerow(row)

print(f"\nログを {out_file} に保存しました！")
