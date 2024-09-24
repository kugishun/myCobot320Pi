from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD

mc = MyCobot(PI_PORT, 115200)
# MyCobot(PI_PORT,PI_BAUD)とするとPI_BAUDの中身である1000000が大きすぎるため反応しない
print(str(PI_PORT) + "," + str(PI_BAUD))
# print(mc.is_connected())
angles = mc.get_angles()
print(angles)
print(str(mc.is_power_on()))
mc.set_color(255, 0, 0)
