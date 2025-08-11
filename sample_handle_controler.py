import pygame
import pygame.locals
import time
import threading

zero = [0, 0, 0, 0, 0, 0]
action = 0
command = -1
status = 0


def control():
    global action, status, command
    select_shaft = 1
    status = 1
    angle = 0
    direction = True
    while True:
        if status == 1:
            if action == 1:
                print("現在の状態を出力します。")
                action = 0
            elif action == 2:
                print("軸が決定されました: {}".format(str(select_shaft)))
                status = 2
            elif action == 4:
                if select_shaft < 6:
                    select_shaft += 1
                elif select_shaft >= 6:
                    select_shaft = 1
                print("選択されている軸: {}".format(str(select_shaft)))
                action = 0
            elif action == 5:
                if select_shaft > 1:
                    select_shaft -= 1
                elif select_shaft <= 1:
                    select_shaft = 6
                print("選択されている軸: {}".format(str(select_shaft)))
                action = 0
            elif action == 6:
                print("action :{}".format(str(action)))
                action = 0

        elif status == 2:
            if action == 1:
                print("現在の状態を出力します。")
                action = 0
            # elif command == 0:
            #     print("軸をマイナス方向に移動します。")
            #     if angle > -90:
            #         angle -= 1
            #         time.sleep(0.5)
            #     # command = -1
            elif command == 1:
                if direction == True:
                    print("軸をプラス方向に移動します。")
                    if angle < 90:
                        angle += 1
                        time.sleep(0.5)
                elif direction == False:
                    print("軸をマイナス方向に移動します。")
                    if angle > -90:
                        angle -= 1
                        time.sleep(0.5)
                # command = -1
            elif action == 3:
                print("軸の選択画面に戻ります。")
                status = 1
                action = 0
            elif action == 6:
                print("action :{}".format(str(action)))
                action = 0
            elif action == 7:
                direction = not direction
                if direction == True:
                    print("プラス方向に移動します。")
                elif direction == False:
                    print("マイナス方向に移動します。")
                action = 0


def main():
    global action, status, command
    flag = 0
    pygame.init()
    pygame.joystick.init()

    try:
        joystick = pygame.joystick.Joystick(0)
    except:
        print("Please connect the handle first.")
        return
    joystick.init()

    done = False

    start_time = 0
    while not done:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                done = True
            elif (
                event_.type == pygame.JOYBUTTONDOWN or event_.type == pygame.JOYBUTTONUP
            ):
                buttons = joystick.get_numbuttons()
                for i in range(buttons):
                    button = joystick.get_button(i)
                    if status == 1:
                        if i == 3:  # Y
                            if button == 1:
                                action = 1
                                print("action 1")
                                break
                        elif i == 0:  # A
                            if button == 1:
                                action = 2
                                print("action 2")
                                break
                        if i == 2:  # X
                            if button == 1:
                                print("action 6")
                                action = 6
                                break
                    elif status == 2:
                        if i == 1:  # B
                            if button == 1:
                                action = 3
                                print("action 3")
                                break
                        if i == 3:  # Y
                            if button == 1:
                                action = 1
                                print("action 1")
                                break
                        elif i == 2:  # X
                            if button == 1:
                                print("action 6")
                                action = 6
                                break

            elif event_.type == pygame.JOYHATMOTION:
                hat = joystick.get_hat(0)
                if status == 1:
                    if hat == (1, 0):
                        action = 4
                        print("action 4")
                        break
                    elif hat == (-1, 0):
                        action = 5
                        print("action 5")
                        break
                elif status == 2:
                    if hat == (0, 1):
                        action = 7
                        print("action 7")
                        break
                    elif hat == (0, -1):
                        action = 7
                        print("action 7")
                        break

            elif event_.type == pygame.JOYAXISMOTION:
                axes = joystick.get_numaxes()
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    if status == 2:
                        # if i == 4:
                        #     if axis > 0.5:
                        #         command = 0
                        #         print("command 0")
                        #         flag = 1
                        #         break
                        #     else:
                        #         if flag == 0:
                        #             command = -1
                        if i == 5:
                            if axis > 0.5:
                                command = 1
                                print("command 1")
                                flag = 1
                                break
                            else:
                                if flag == 0:
                                    command = -1
                flag = 0


if __name__ == "__main__":
    t = threading.Thread(target=control)
    t.daemon = True
    t.start()
    print("test")
    main()
