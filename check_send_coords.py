from pymycobot.mycobot320 import MyCobot320
import time
# import the project package
# Initiate a MyPalletizer object
mc = MyCobot320("/dev/ttyAMA0", 115200)

# # Get the current coordinates and pose of the head
# coords = mc.get_coords()
# print(coords)

mc.init_electric_gripper()
print(mc.get_gripper_value())

#Plan the route at random, let the head reach the coordinates of [57.0, -107.4, 316.3] in an non-linear manner at the speed is 80mm/s
print("first")
mc.send_coords([22.82, -246.83, 421.77, -63.78, 85.64, 17.65],50,1)
# wait for 2 seconds
time.sleep(4)

# Plan the route at random, let the head reach the coordinates of [207.9, 47, 49.3,-159.69] in an non-linear manner at the speed is 80mm/s
print("second")
mc.send_coords([-322.23, -206.54, 180.52, 64.37, 162.74, -173.04], 80, 0)
# wait for 2 seconds
time.sleep(4)

#To change only the x-coordinate of the head, set the x-coordinate of the head to 20. Let it plan the route at random and move the head to the changed position at a speed of 70mm/s
print("third")
mc.send_coords([98.14, 232.62, 166.24, -138.59, -147.04, -50.08], 80, 0)

time.sleep(4)
print("finish")