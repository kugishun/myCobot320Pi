from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time

mc = MyCobot("/dev/ttyAMA0", 115200)
mc.init_eletric_gripper()

mc.power_off()
mc.power_on()

mc.send_angles([0, 0, 0, 0, 0, 0], 50)
time.sleep(5)

mc.send_angles([-18, 84.5, 20, 24.5, 0, 96], 50)
time.sleep(5)
mc.set_eletric_gripper(1)
mc.set_eletric_gripper(1)
mc.set_eletric_gripper(1)

mc.send_angles([-18, 85, 3, 24.5, 0, 96], 50)
time.sleep(10)
mc.send_angles([-18, 84.5, 20, 24.5, 0, 96], 50)
time.sleep(10)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
mc.send_angless([0, 0, 0, 0, 0, 0], 50)
time.sleep(5)
