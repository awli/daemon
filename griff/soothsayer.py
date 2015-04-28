"""Soothsayer is a module for interpreting things that come into ansible
"""
import ansible
from ansible import AMessage
from multiprocessing import Process, Manager
from threading import Thread

callbacks = {}

# on, like in EventEmitters
def on(msg_type, fn):
    if msg_type in callbacks:
        callbacks[msg_type].append(fn)
    else:
        callbacks[msg_type] = [fn]

def main():
    while True:
        msg = ansible.recv(block=True)
        if isinstance(msg, AMessage):
            fns = callbacks.get(msg.msg_type, [])
            for f in fns:
                f(msg)

Thread(target=main).start()
