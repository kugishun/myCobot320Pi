import time
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT

mc = MyCobot("/dev/ttyAMA0", 115200)


def check_status():
    print("Power status: ", mc.is_power_on())
    print("Angles: ", mc.get_angles())


if __name__ == "__main__":
    mc.power_off()
    time.sleep(1)
    mc.power_on()
    time.sleep(3)  # アーム初期化を待つ

    print("=== Initial Check ===")
    check_status()

    print("=== Moving Arm ===")
    mc.send_angles([10, 10, 10, 10, 10, 10], 50)
    time.sleep(2)

    print("=== After Movement ===")
    check_status()
