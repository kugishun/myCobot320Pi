from pymycobot import MyCobot320
import time
mc = MyCobot320("/dev/ttyAMA0", 115200)#填写机械臂的串口号
mc.set_pro_gripper_torque(14,10)#设置夹爪的力矩值
print(mc.get_pro_gripper_torque(14))#打印设置完的夹爪力矩值
mc.set_pro_gripper_open(14)#先让夹爪完全打开
start_angles=[19.68, -1.23, -91.4, -0.52, 90.08, 60.29]
target_coords=[[231.3, -61.3, 232.7, 178.35, -2.7, -130.56],[231.3, 65.3, 232.7, 178.35, -2.7, -130.56]]
end_angles=[80,0,-85,0,90,60]
for i in range(len(target_coords)):
    mc.sync_send_angles(start_angles,50)
    mc.send_coords(target_coords[i],100,1)
    time.sleep(2)
    mc.send_coord(3,165,50)
    time.sleep(2)
    mc.set_pro_gripper_close(14)
    time.sleep(2)
    mc.send_coords(target_coords[i],100,1)
    mc.sync_send_angles(end_angles,100)
    mc.set_pro_gripper_open(14)
    time.sleep(2)