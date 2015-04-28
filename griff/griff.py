from threading import Thread

import gamepad
gamepad_thread = Thread(target=gamepad.update_thread)
gamepad_thread.start()

import usercode
# for now, we assume that the user thread won't do anything horrifyingly bad
# and run everything in one process.
user_thread = Thread(target=usercode.teleop)
user_thread.start()
