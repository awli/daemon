"""Soothsayer is a module for interpreting things that come into ansible
"""
import ansible
from ansible import AMessage
from multiprocessing import Process, Manager

actors = {}

# on, like in EventEmitters
def on(msg_type, actor):
    if msg_type in actors:
        actors[msg_type].append(actor)
    else:
        actors[msg_type] = [actor]

def main(actors):
    while True:
        msg = ansible.recv(block=True)
        if isinstance(msg, AMessage):
            print 'got AMessage'
            target_actors = actors.get(msg.msg_type, [])
            for actor in target_actors:
                print 'calling thread'
                actor(msg)

Process(target=main, args=(actors,)).start()
