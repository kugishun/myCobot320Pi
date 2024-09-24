from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
from pymycobot import (
    PI_PORT,
    PI_BAUD,
)  # When using the Raspberry Pi version of mycobot, you can refer to these two variables to initialize MyCobot
import time

# MyCobot class initialization requires two parameters:
#   The first is the serial port string, such as:
#       linux:  "/dev/ttyUSB0"
#          or "/dev/ttyAMA0"
#       windows: "COM3"
#   The second is the baud rate::
#       M5 version is:  115200
#
#    Example:
#       mycobot-M5:
#           linux:
#              mc = MyCobot("/dev/ttyUSB0", 115200)
#          or mc = MyCobot("/dev/ttyAMA0", 115200)
#           windows:
#              mc = MyCobot("COM3", 115200)
#       mycobot-raspi:
#           mc = MyCobot(PI_PORT, PI_BAUD)
#
# Initiate a MyCobot object
# Create object code here for windows version
mc = MyCobot("/dev/ttyAMA0", 115200)
angles = mc.get_angles()
print(angles)  # Operation confirmation

# By passing the angle parameter, let each joint of the robotic arm move to the position corresponding to [0, 0, 0, 0, 0, 0]
mc.send_angles([0, 0, 0, 0, 0, 0], 50)

# Set the waiting time to ensure that the robotic arm has reached the specified position
time.sleep(12.5)

# Move joint 1 to the 90 position
mc.send_angle(Angle.J1.value, 90, 10)
# Set the waiting time to ensure that the robotic arm has reached the specified position
time.sleep(10)


# The following code can make the robotic arm swing left and right
# set the number of loops
num = 5

# while num > 0:

#     # Move joint 2 to the 50 position
#     mc.send_angle(Angle.J2.value, 50, 50)

#     # Set the waiting time to ensure that the robotic arm has reached the specified position
#     time.sleep(1.5)

#     # Move joint 2 to the -50 position
#     mc.send_angle(Angle.J2.value, -50, 50)

#     # Set the waiting time to ensure that the robotic arm has reached the specified position
#     time.sleep(1.5)

#     num -= 1

# # Make the robotic arm retract. You can manually swing the robotic arm, and then use the get_angles() function to get the coordinate sequence,
# # use this function to let the robotic arm reach the position you want.
# mc.send_angles([88.68, -138.51, 155.65, -128.05, -9.93, -15.29], 50)
mc.send_angles(angles, 10)

# Set the waiting time to ensure that the robotic arm has reached the specified position
time.sleep(12.5)

# Let the robotic arm relax, you can manually swing the robotic arm
mc.release_all_servos()
