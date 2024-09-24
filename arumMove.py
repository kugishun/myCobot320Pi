from pymycobot.mycobot import MyCobot
from pymycobot import (
    PI_PORT,
    PI_BAUD,
)  # When using the Raspberry Pi version of myCobot, you can refer to these two variables for MyCobot initialization
import time

if __name__ == "__main__":
    # Initialize a MyCobot object
    mc = MyCobot(PI_PORT, 115200)
    # Set the start time
    start = time.time()
    # Let the robot arm move to the specified position
    mc.send_angles([-1.49, 115, -153.45, 30, -33.42, 137.9], 80)
    # Check whether it move to the specified positon
    while not mc.is_in_position([-1.49, 115, -153.45, 30, -33.42, 137.9], 0):
        # Restore the movement of the robot arm
        mc.resume()
        # Let the robot arm move 0.5s
        time.sleep(0.5)
        # Pause the movement of the robot arm
        mc.pause()
        # Check if the movement timed out
        if time.time() - start > 3:
            break
    # Set start time
    start = time.time()
    # Let the movement last 30 seconds
    while time.time() - start < 30:
        # Let the robot arm reach this position quickly
        mc.send_angles([-1.49, 115, -153.45, 30, -33.42, 137.9], 80)
        # Set the color of the light to[0,0,50]
        mc.set_color(0, 0, 50)
        time.sleep(0.7)
        # Let the robot arm reach this position quickly
        mc.send_angles([-1.49, 55, -153.45, 80, 33.42, 137.9], 80)
        # Set the color of the light to[0,50,0]
        mc.set_color(0, 50, 0)
        time.sleep(0.7)

    # mc.release_all_servos()
