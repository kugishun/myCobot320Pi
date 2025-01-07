import time
from pymycobot.mycobot import MyCobot

# 使用するポートとボーレートを指定
PORT = "/dev/ttyAMA0"  # 必要に応じて変更
BAUD = 115200

mc = MyCobot(PORT, BAUD)

# 通信確認
print("Checking communication...")
time.sleep(2)

power_status = mc.is_power_on()
if power_status == -1:
    print("Communication failed. Please check the port and connection.")
else:
    print("Power status: ", power_status)

# アームの初期化
mc.power_on()
time.sleep(2)

print("Angles: ", mc.get_angles())
