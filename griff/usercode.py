# example usercode
import api
import random

def teleop():
    while True:
        api.Robot.motors[0].set_speed(random.randint(0, 25))