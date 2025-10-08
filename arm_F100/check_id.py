from elegripper_modbus import Gripper

for test_id in range(1, 16):
    try:
        g = Gripper("/dev/ttyCH343USB0", baudrate=115200, id=test_id)
        print(f"Trying ID {test_id}: ", g.get_gripper_Id())
    except Exception as e:
        print(f"ID {test_id} failed:", e)
