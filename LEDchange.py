from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD

mc = MyCobot("/dev/ttyAMA0", 115200)
print(str(PI_PORT) + "," + str(PI_BAUD))
# print(mc.is_connected())
angles = mc.get_angles()
print(angles)
mc.set_color(255, 0, 0)
