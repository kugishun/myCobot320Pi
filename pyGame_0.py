import pygame
import pygame.locals

pygame.init()
pygame.joystick.init()

num_joysticks = pygame.joystick.get_count()

if num_joysticks > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print("Controller connected:", controller.get_name())
else:
    print("No controller detected.")
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
