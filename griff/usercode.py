# example usercode
import gamepad, Robot # todo lowercase Robot

def teleop():
    while True:
        Robot.motors[0].set_speed(gamepad.axes[0])