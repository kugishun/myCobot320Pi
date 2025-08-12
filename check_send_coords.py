from pymycobot.mycobot320 import MyCobot320
import time, math

mc = MyCobot320("/dev/ttyAMA0", 115200)

# --- 便利関数たち -----------------------------------------------------------
def get_current_angles_deg(mc):
    """現在関節角をdegで取得（使えるAPIに応じてフォールバック）"""
    try:
        ang = mc.get_angles_plan()  # あればこれがdeg
        if ang and len(ang) == 6:
            return ang
    except Exception:
        pass
    try:
        rad = mc.get_radians()      # rad -> deg
        if rad and len(rad) == 6:
            return [r * 180.0 / math.pi for r in rad]
    except Exception:
        pass
    # 最後の手段：ゼロで初期化（IKの初期解としては弱い）
    return [0, 0, 0, 0, 0, 0]

def within_workspace(coords):
    """座標の簡易クリップ（myCobot320の仕様範囲）"""
    x,y,z,rx,ry,rz = coords
    x = max(-350.0, min(350.0, x))
    y = max(-350.0, min(350.0, y))
    z = max(-41.0,  min(523.9, z))
    rx = max(-180.0, min(180.0, rx))
    ry = max(-180.0, min(180.0, ry))
    rz = max(-180.0, min(180.0, rz))
    return [x,y,z,rx,ry,rz]

def solve_and_move(mc, coords, speed=50, mode=1, timeout=20, verbose=True):
    """
    1) 作業空間にクリップ
    2) IKを事前に試す（解ければ send_angles / 同期版）
    3) 解けなければ send_coords / 同期版 にフォールバック
    """
    coords = within_workspace(coords)
    cur = get_current_angles_deg(mc)
    try:
        sol = mc.solve_inv_kinematics(coords, cur)
    except Exception as e:
        sol = None
        if verbose: print("[IK] solve_inv_kinematics error:", e)

    # IK成功時（6要素の角度リストが返る前提）
    if isinstance(sol, list) and len(sol) == 6 and all(isinstance(a, (int,float)) for a in sol):
        if verbose: print("[IK] solved -> send_angles", sol)
        ok = mc.sync_send_angles(sol, speed, timeout=timeout)
        return ("angles", ok)

    # 解けない/未対応 → そのまま座標で
    if verbose:
        print("[IK] no solution -> fallback to send_coords", coords)
    ok = mc.sync_send_coords(coords, speed, mode, timeout=timeout)
    return ("coords", ok)
# ---------------------------------------------------------------------------

# フレームなどを明示（必要に応じて）
try:
    mc.set_reference_frame(0)   # 0=base
    mc.set_end_type(1)          # 1=tool（ツール先端をTCPにしたい場合）
    mc.set_movement_type(1)     # 1=直線(movel), 0=関節(moveJ)
    mc.set_fresh_mode(0)        # 0=キュー実行（順次実行）
except Exception:
    pass

print("first")
solve_and_move(mc, [22.82, -246.83, 421.77, -63.78, 85.64, 17.65], speed=50, mode=1, timeout=20)
time.sleep(1)  # 余裕を少し

print("second")
solve_and_move(mc, [-322.23, -206.54, 180.52, 64.37, 162.74, -173.04], speed=80, mode=0, timeout=20)
time.sleep(1)

print("third")
solve_and_move(mc, [98.14, 232.62, 166.24, -138.59, -147.04, -50.08], speed=80, mode=0, timeout=20)

print("finish")
