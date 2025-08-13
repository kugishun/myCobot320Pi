from pymycobot.mycobot320 import MyCobot320
from pymycobot import PI_PORT, PI_BAUD
from pymycobot.genre import Angle
import time

mc = MyCobot320(PI_PORT, 115200)

mc.power_off()
mc.power_on()

mc.send_angles([0, 0, 0, 0, 0, 0], 50)
# print(type(mc.get_angles))
# mc.init_electric_gripper()
time.sleep(2)
mc.send_coords([0, -153, 523, 0, 0, -180], 50, 1)
time.sleep(2)
# flag = mc.is_gripper_moving()
# print("Is gripper moving: {}".format(flag))
print(mc.get_angles())
coords = mc.get_coords()
print(f"get_coords():{coords}")
# mc.set_gripper_state(0, 50)
# mc.set_electric_gripper(0)
# mc.set_electric_gripper(0)
# mc.set_electric_gripper(0)
# time.sleep(3)
# mc.set_electric_gripper(1)  # 1 is close ,0 is open
# mc.set_electric_gripper(1)
# mc.set_electric_gripper(1)
# mc.set_gripper_value(100, 50)  # value is 0 to 256, speed is 0 to 100
# time.sleep(2)

# mc.release_all_servos()
