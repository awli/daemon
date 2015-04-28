# example usercode
from api import Robot, Gamepad

def teleop():
    while True:
        Robot.motors[0].set_speed(Gamepad.axes[0])
