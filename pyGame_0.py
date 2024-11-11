import pygame
import pygame.locals
import time
import threading

# pygame.init()
# pygame.joystick.init()

# num_joysticks = pygame.joystick.get_count()

# if num_joysticks > 0:
#     controller = pygame.joystick.Joystick(0)
#     controller.init()
#     print("Controller connected:", controller.get_name())
# else:
#     print("No controller detected.")


def main():
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
                    print("i value:", i)
                    print("button--->", button)
            elif event_.type == pygame.JOYAXISMOTION:
                axes = (
                    joystick.get_numaxes()
                )  # パッドについている軸(スティック等)の数を取得
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    print("i value: {} axis value: {}".format(i, axis))
            elif event_type == pygame.JOYHATMOTION:  # 十字キーを検知
                hat = joystick.get_hat(0)
                print("hat:", str(hat))

    pygame.quit()


if __name__ == "__main__":
    main()


# To get the number of axes, buttons, and hats on the controller
# num_axes = joystick.get_numaxes()
# num_buttons = joystick.get_numbuttons()
# num_hats = joystick.get_numhats()

# # To read the input from the axes
# axis_0 = joystick.get_axis(0)
# axis_1 = joystick.get_axis(1)
# # ...

# # To read the input from the buttons (returns 1 if pressed, 0 if not pressed)
# button_0 = joystick.get_button(0)
# button_1 = joystick.get_button(1)
# # ...

# # To read the input from the hats (returns a tuple in the form (x, y))
# hat_0 = joystick.get_hat(0)
