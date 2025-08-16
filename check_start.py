from pymycobot.mycobot320 import MyCobot320
from pymycobot import PI_PORT, PI_BAUD
import time

mc = MyCobot320(PI_PORT, 115200)

mc.send_angles([0, 0, 0, 0, 0, 0], 50)

coords = mc.get_coords()
print(f"get_coords():{coords}")