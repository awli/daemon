from multiprocessing import Process
import api
import usercode

p = Process(target=usercode.teleop)

p.start()
p.join()