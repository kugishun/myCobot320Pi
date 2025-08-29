import numpy as np, math, itertools

# ===== your measured dataset =====
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

# ===== DH & FK (myCobot 320) =====
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

DH = [
    (0,     90, 131.56),
    (-110,   0,   0   ),
    (-96,    0,   0   ),
    (0,     90, 131.25),
    (0,    -90,  96   ),
    (0,      0, 156.4 )
]

def fk(j):
    T = np.eye(4)
    for (a, alpha, d), th in zip(DH, j):
        T = T @ dh(a, alpha, d, th)
    return T[:3,:3]

# ===== helpers =====
def wrap180(a): return (a+180.0)%360.0 - 180.0

def euler_from_R(R, order, intrinsic):
    """Return angles [a,b,c] for given order (e.g. 'XYZ'). 
       intrinsic=True -> intrinsic rotations; False -> extrinsic.
       This enumerates all 6 orders with stable formulas."""
    ax = order[0]; ay = order[1]; az = order[2]
    # map axis char -> index
    idx = {'X':0, 'Y':1, 'Z':2}
    # build elemental rotation matrices functions
    def Rx(t):
        c,s = math.cos(t), math.sin(t)
        return np.array([[1,0,0],[0,c,-s],[0,s,c]])
    def Ry(t):
        c,s = math.cos(t), math.sin(t)
        return np.array([[c,0,s],[0,1,0],[-s,0,c]])
    def Rz(t):
        c,s = math.cos(t), math.sin(t)
        return np.array([[c,-s,0],[s,c,0],[0,0,1]])
    Rm = {'X':Rx, 'Y':Ry, 'Z':Rz}

    # We implement decomposition by numeric search (small LM) to be robust
    # Initialize angles via naive guess (0,0,0)
    a=b=c=0.0
    # simple Gauss-Newton iterations
    for _ in range(50):
        A,B,C = a,b,c
        RA, RB, RC = Rm[ax](A), Rm[ay](B), Rm[az](C)
        if intrinsic:
            Rhat = RA @ RB @ RC
        else:
            Rhat = RC @ RB @ RA
        E = Rhat.T @ R  # right-invariant error
        # log map (approx) to get small-angle error vector
        w = np.array([E[2,1]-E[1,2], E[0,2]-E[2,0], E[1,0]-E[0,1]])/2.0
        # small step on each parameter axis numerically
        def err_with(deltaA, deltaB, deltaC):
            RA2, RB2, RC2 = Rm[ax](A+deltaA), Rm[ay](B+deltaB), Rm[az](C+deltaC)
            if intrinsic:
                R2 = RA2 @ RB2 @ RC2
            else:
                R2 = RC2 @ RB2 @ RA2
            E2 = R2.T @ R
            w2 = np.array([E2[2,1]-E2[1,2], E2[0,2]-E2[2,0], E2[1,0]-E2[0,1]])/2.0
            return w2
        eps = 1e-4
        Ja = (err_with(eps,0,0)-w)/eps
        Jb = (err_with(0,eps,0)-w)/eps
        Jc = (err_with(0,0,eps)-w)/eps
        J = np.column_stack([Ja,Jb,Jc])
        # solve least squares J*delta = -w
        try:
            delta, *_ = np.linalg.lstsq(J, -w, rcond=None)
        except np.linalg.LinAlgError:
            break
        a += delta[0]; b += delta[1]; c += delta[2]
        if np.linalg.norm(delta) < 1e-8: break
    return np.degrees([a,b,c])

# 24 right-handed orthonormal bases (permutation with sign) -> rotation matrices
def all_frame_rotations():
    mats = []
    axes = np.eye(3)
    for perm in itertools.permutations([0,1,2],3):
        P = axes[:,perm]
        for signs in itertools.product([1,-1],[1,-1],[1,-1]):
            R = P @ np.diag(signs)
            if np.linalg.det(R) > 0.9:   # keep proper rotations
                mats.append(R)
    # deduplicate
    uniq = []
    for M in mats:
        key = tuple(np.round(M,6).flatten())
        if key not in {tuple(np.round(U,6).flatten()) for U in uniq}:
            uniq.append(M)
    return uniq

FRAMES = all_frame_rotations()
orders = ["XYZ","XZY","YXZ","YZX","ZXY","ZYX"]
best = []

for order in orders:
    for intrinsic in [True, False]:
        for Qpre in FRAMES:
            for Qpost in FRAMES:
                # try per-axis sign flip (angle mapping)
                for sgn in itertools.product([1,-1],[1,-1],[1,-1]):
                    preds = []
                    meas  = []
                    for joints, m in DATA:
                        R = fk(joints)
                        Rrep = Qpre @ R @ Qpost
                        ang = euler_from_R(Rrep, order, intrinsic) * np.array(sgn)
                        preds.append(ang)
                        meas.append(m)
                    preds = np.vstack(preds)
                    meas  = np.vstack(meas)
                    # fit optimal constant offset per axis by least squares on wrapped angles
                    # unwrap by picking offsets that minimize squared error around mean
                    off = np.zeros(3)
                    for k in range(3):
                        # brute-force search offset near multiples of 90 to capture wrap
                        cands = np.linspace(-180,180,721)  # 0.5°刻み
                        errs = []
                        for o in cands:
                            d = (meas[:,k] - (preds[:,k]+o) + 180)%360 - 180
                            errs.append(np.mean(d*d))
                        off[k] = cands[int(np.argmin(errs))]
                    pred_off = preds + off
                    diff = (meas - pred_off + 180)%360 - 180
                    rmse = math.sqrt(np.mean(diff*diff))
                    best.append((rmse, order, intrinsic, sgn, off, Qpre, Qpost))

best.sort(key=lambda x:x[0])
print("=== top 5 models ===")
for i in range(5):
    rmse, order, intrinsic, sgn, off, Qpre, Qpost = best[i]
    print(f"[{i}] RMSE={rmse:.3f}°, order={order}, intrinsic={intrinsic}, sgn={sgn}, off={off}")
    print(" Qpre=\n", np.round(Qpre,3))
    print(" Qpost=\n", np.round(Qpost,3))

# 予測を確認（最良モデルで一覧表示）
rmse, order, intrinsic, sgn, off, Qpre, Qpost = best[0]
print("\n--- Check with best model ---")
for joints, m in DATA:
    R = fk(joints); Rrep = Qpre @ R @ Qpost
    ang = euler_from_R(Rrep, order, intrinsic) * np.array(sgn) + off
    ang = ((ang+180)%360)-180
    print("joints=", joints, " meas=", np.round(m,2), " pred=", np.round(ang,2))
print("\nBest model summary:",
      f"order={order}, intrinsic={intrinsic}, sgn={sgn}, off={np.round(off,2)}")
