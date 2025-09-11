import socket
import json
import threading
import queue
import time
from pymycobot.mycobot320 import MyCobot320
from MyHand import MyGripper_H100

# ====== UDP受信設定 ======
IP = "0.0.0.0"
PORT = 7010

# ====== キュー（受信データを処理スレッドに渡す） ======
data_queue = queue.Queue()

def udp_receiver():
    """UDPでデータを受信してキューに格納"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    print(f"[myCobot Server] Listening on {IP}:{PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode("utf-8"))
            data_queue.put(msg)   # キューに追加
        except Exception as e:
            print("UDP recv error:", e)

def data_processor():
    """キューからデータを取り出して処理"""
    mc = MyCobot320("/dev/ttyAMA0", 115200)  # 実機制御はここで初期化
    hand=MyGripper_H100("/dev/ttyCH343USB0")
    mc.power_on()
    hand.set_gripper_pose(4,15)

    while True:
        try:
            msg = data_queue.get()  # データを1件取り出す（ブロッキング）
            
            if "angles" in msg:
                angles = msg["angles"]
                print("[Processor] angles:", angles)
                mc.send_angles(angles, 30)

            if "gripper" in msg:
                gripper = msg["gripper"]
                print("[Processor] gripper:", gripper)
                hand.set_gripper_joint_angle(1, int(gripper[2]))
                hand.set_gripper_joint_angle(2, int(gripper[1]))
                hand.set_gripper_joint_angle(3, int(gripper[0]))

        except Exception as e:
            print("Process error:", e)
        time.sleep(0.01)  # CPU負荷を抑えるため少し待機

if __name__ == "__main__":
    # 受信スレッド
    t1 = threading.Thread(target=udp_receiver, daemon=True)
    t1.start()

    # 処理スレッド
    t2 = threading.Thread(target=data_processor, daemon=True)
    t2.start()

    # メインは待機
    while True:
        time.sleep(1)
