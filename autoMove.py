from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time

mc = MyCobot("/dev/ttyAMA0", 115200)
mc.init_eletric_gripper()

mc.power_off()
mc.power_on()

mc.send_angles([0, 0, 0, 0, 0, 0], 50)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
time.sleep(5)
mc.send_angles([-18, 85, 3, 24.5, 0, 96], 40)
time.sleep(5)
mc.send_angles([-18, 84.5, 18, 24.5, 0, 96], 30)
time.sleep(5)

while True:
    user_input = input("Enter 1 to start the next sequence: ")
    if user_input == "1":
        break

mc.set_eletric_gripper(1)
mc.set_eletric_gripper(1)
mc.set_eletric_gripper(1)
time.sleep(5)
mc.send_angles([-18, 85, 3, 24.5, 0, 96], 30)
time.sleep(5)
mc.send_angles([-18, 84.5, 18, 24.5, 0, 96], 40)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
mc.send_angles([0, 0, 0, 0, 0, 0], 50)
time.sleep(5)
