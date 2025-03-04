from pymycobot.mycobot320 import MyCobot320
from pymycobot.genre import Angle
import time

mc = MyCobot320("/dev/ttyAMA0", 115200)
mc.init_electric_gripper()

mc.power_off()
mc.power_on()

mc.send_angles([0, 0, 0, 0, 0, 0], 50)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
time.sleep(5)
mc.send_angles([-18, 85, 3, 24.5, 0, 96], 40)
time.sleep(5)
mc.send_angles([-18, 84.5, 18, 24.5, 0, 96], 30)
time.sleep(5)

while True:
    user_input = input("Enter 1 to start the next sequence: ")
    if user_input == "1":
        break

mc.set_electric_gripper(1)
mc.set_electric_gripper(1)
mc.set_electric_gripper(1)
mc.set_electric_gripper(1)
mc.set_electric_gripper(1)
time.sleep(5)
mc.send_angles([-18, 85, 3, 24.5, 0, 96], 30)
time.sleep(5)
mc.send_angles([-18, 84.5, 18, 24.5, 0, 96], 40)
time.sleep(5)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.set_electric_gripper(0)
mc.send_angles([0, 0, 0, 0, 0, 0], 50)
time.sleep(5)
