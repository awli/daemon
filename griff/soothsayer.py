"""Soothsayer is a module for interpreting things that come into ansible

You pass Soothsayer pykka actors for messages.
"""
import ansible
from ansible import AMessage
from multiprocessing import Process, Manager
from threading import Thread

actors = {}

# on, like in EventEmitters
def on(msg_type, actor):
    if msg_type in actors:
        actors[msg_type].append(actor)
    else:
        actors[msg_type] = [actor]

def main():
    while True:
        msg = ansible.recv(block=True)
        if isinstance(msg, AMessage):
            target_actors = actors.get(msg.msg_type, [])
            for actor in target_actors:
                assert isinstance(msg.content, dict)
                actor.tell(msg.content)

Thread(target=main).start()
