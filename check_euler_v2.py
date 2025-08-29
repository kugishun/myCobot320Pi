import numpy as np, math, itertools

# ====== DH & FK ======
def dh(a, alpha, d, theta):
    A = math.radians(alpha); T = math.radians(theta)
    ca, sa = math.cos(A), math.sin(A)
    ct, st = math.cos(T), math.sin(T)
    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0 ,     sa,     ca,    d],
        [0 ,      0,      0,    1]
    ], float)

# myCobot 320（代表値：mm）
DH = [
    (0,     90, 131.56),  # J1
    (-110,   0,   0   ),  # J2
    (-96,    0,   0   ),  # J3
    (0,     90, 131.25),  # J4
    (0,    -90,  96   ),  # J5
    (0,      0, 156.4 )   # J6
]

def fk(j):
    T = np.eye(4)
    for (a, alpha, d), th in zip(DH, j):
        T = T @ dh(a, alpha, d, th)
    return T[:3,:3]

# ====== Euler converters ======
def euler_xyz(R):
    sy = -R[2,0]; cy = math.sqrt(max(0.0,1-sy*sy))
    if cy > 1e-8:
        x = math.degrees(math.atan2(R[2,1], R[2,2]))
        y = math.degrees(math.asin(sy))
        z = math.degrees(math.atan2(R[1,0], R[0,0]))
    else:
        x = math.degrees(math.atan2(-R[1,2], R[1,1])); y = math.degrees(math.asin(sy)); z = 0.0
    return np.array([x,y,z])

def euler_zyx(R):
    sy = math.sqrt(R[0,0]**2 + R[1,0]**2)
    if sy > 1e-8:
        x = math.degrees(math.atan2(R[2,1], R[2,2]))
        y = math.degrees(math.atan2(-R[2,0], sy))
        z = math.degrees(math.atan2(R[1,0], R[0,0]))
    else:
        x = math.degrees(math.atan2(-R[1,2], R[1,1])); y = math.degrees(math.atan2(-R[2,0], sy)); z = 0.0
    return np.array([x,y,z])

def euler_zyz(R):
    c = R[2,2]
    if abs(c) < 1-1e-8:
        beta  = math.degrees(math.acos(c))
        alpha = math.degrees(math.atan2(R[1,2], R[0,2]))
        gamma = math.degrees(math.atan2(R[2,1], -R[2,0]))
    else:
        beta = 0.0 if c>0 else 180.0
        alpha = 0.0
        gamma = math.degrees(math.atan2(R[0,1], R[0,0]))
    return np.array([alpha,beta,gamma])

EULERS = {
    "XYZ": euler_xyz,
    "ZYX": euler_zyx,
    "ZYZ": euler_zyz,
}

# ====== candidate fixed rotations (pre/post) ======
def Rx(d): a=math.radians(d); c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(d): a=math.radians(d); c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(d): a=math.radians(d); c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])

rots_90 = [np.eye(3), Rx(90), Rx(-90), Ry(90), Ry(-90), Rz(90), Rz(-90), Rz(180)]
# 2段までの合成も少し含める（軽め）
cands = set()
for A in rots_90:
    cands.add(tuple(A.round(6).flatten()))
    for B in rots_90:
        M = (A@B).round(6)
        cands.add(tuple(M.flatten()))
CANDS = [np.array(c).reshape(3,3) for c in cands]

# ====== helpers ======
def wrap180(a): 
    a = (a+180.0)%360.0 - 180.0
    return a

def ang_err(a,b):  # elementwise wrapped error
    return wrap180(a-b)

# ====== your measurements ======
# configs: (j1..j6 in deg)  -> measured [rx,ry,rz]
DATA = [
    ((0,0,0,0,0,0),     np.array([-90.0, -0.52, -179.91])),
    ((30,0,0,0,0,0),    np.array([-90.0, -0.35, -149.67])),
    ((-30,0,0,0,0,0),   np.array([-90.0, -0.43,  150.29])),
    ((0,30,0,0,0,0),    np.array([-90.0, 31.55,  179.32])),
    ((0,-30,0,0,0,0),   np.array([-90.0,-32.25, -179.49])),
    ((0,0,30,0,0,0),    np.array([-90.0, 31.20,  179.67])),
    ((0,0,-30,0,0,0),   np.array([-90.0,-31.81, -179.49])),
    ((0,0,0,30,0,0),    np.array([-90.0, 30.40,  179.68])),
    ((0,0,0,-30,0,0),   np.array([-90.0,-31.02, -179.58])),
    ((0,0,0,0,30,0),    np.array([-90.0, -1.01, -150.02])),
    ((0,0,0,0,90,0),    np.array([-90.0, -1.01,  -90.17])),
    ((0,0,0,0,-30,0),   np.array([-90.0,  0.28,  150.20])),
    ((0,0,0,0,-90,0),   np.array([-90.0,  0.20,  122.60])),
    ((0,0,0,0,0,30),    np.array([-90.0, 29.53, -179.91])),
    ((0,0,0,0,0,-30),   np.array([-90.0,-30.32, -179.91])),
]

# ====== search ======
best = []
for order, func in EULERS.items():
    for Qpre in CANDS:
        for Qpost in CANDS:
            # optional per-axis offsets in {0, ±180}（rzの±180が効くことが多い）
            for offs in [(0,0,0),(0,0,180),(0,0,-180),(180,0,0),(0,180,0),(0,-180,0)]:
                sse = 0.0; n=0
                for joints, meas in DATA:
                    R = fk(joints)
                    Rrep = Qpre @ R @ Qpost
                    pred = func(Rrep)
                    pred = np.array([wrap180(pred[0]+offs[0]), wrap180(pred[1]+offs[1]), wrap180(pred[2]+offs[2])])
                    err = ang_err(meas, pred)
                    sse += float((err**2).sum()); n += 3
                rmse = math.sqrt(sse/n)
                best.append((rmse, order, offs, Qpre, Qpost))
best.sort(key=lambda x: x[0])

print("==== top candidates ====")
for i in range(5):
    rmse, order, offs, Qpre, Qpost = best[i]
    print(f"[{i}] RMSE={rmse:.3f}  order={order}  offs(deg)={offs}")
    # 簡略に Qpre/Qpost の種類を推定表示
    print("  Qpre≈\n", np.array(Qpre))
    print("  Qpost≈\n", np.array(Qpost))
