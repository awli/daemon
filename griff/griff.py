from multiprocessing import Process
import Robot
import usercode

# set up proxy objects
robot_proxy = api.Robot # temporary

p = Process(target=usercode.teleop, \
    args=(robot_proxy, gamepad_proxy))

p.start()
p.join()