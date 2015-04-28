# example usercode
def teleop(robot, gamepad):
    while True:
        robot.motors[0].set_speed(gamepad.axes[0])
