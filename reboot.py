from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
from pymycobot.genre import Angle
import time

mc = MyCobot(PI_PORT, 115200)

mc.power_off()
mc.power_on()

mc.send_angles([-124, 130, -4, -2, 7, -1.5], 50)
time.sleep(12.5)

# mc.release_all_servos()
