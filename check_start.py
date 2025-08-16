from pymycobot.mycobot320 import MyCobot320
from pymycobot import PI_PORT, PI_BAUD
import time

mc = MyCobot320(PI_PORT, 115200)

mc.send_angles([0, 0, 0, 0, 0, 0], 50)
time.sleep(1)
coords = mc.get_coords()
print(f"get_coords():{coords}")

mc.send_angles([90, 0, 0, 0, 0, 0], 50)
time.sleep(1)
coords = mc.get_coords()
print(f"get_coords():{coords}")

mc.send_angles([-90, 0, 0, 0, 0, 0], 50)
time.sleep(2)
coords = mc.get_coords()
print(f"get_coords():{coords}")