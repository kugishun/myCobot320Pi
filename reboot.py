from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
from pymycobot.genre import Angle
import time

mc = MyCobot(PI_PORT, 115200)

mc.power_off()
mc.power_on()

mc.send_angles([0, 0, 0, 0, 0, 0], 50)
print(type(mc.get_angles))
time.sleep(5)
flag = mc.is_gripper_moving()
print("Is gripper moving: {}".format(flag))
# mc.set_gripper_state(0, 50)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
mc.set_eletric_gripper(0)
time.sleep(3)
mc.set_eletric_gripper(1)  # 1 is close ,0 is open
mc.set_eletric_gripper(1)
mc.set_eletric_gripper(1)
mc.set_gripper_value(100, 50)  # value is 0 to 256, speed is 0 to 100
time.sleep(2)

# mc.release_all_servos()
