import zmq, yaml
from multiprocessing import Process
from multiprocessing import Queue as ProcessQueue
from threading import Thread, Lock
from Queue import Queue, Empty

class AMessage(object):
    """Convenience class for sending Ansible Messages

    import ansible
    from ansible import AMessage

    ansible.send(AMessage('msg_type', {}))

    """

    def __init__(self, msg_type, content):
        assert isinstance(msg_type, basestring)
        self.msg_type = msg_type
        self.content = content

    @property
    def as_dict(self):
        return {
            'header': {'msg_type': self.msg_type},
            'content': self.content
        }

    def __str__(self):
        return "<AMessage type '%s'>" % self.msg_type

    def __repr__(self):
        return "AMessage(%s, %s)" % (self.msg_type, repr(self.content))

# Sender process.
def sender(port, send_queue):
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://127.0.0.1:%d" % port)
    while True:
        msg = send_queue.get()
        if isinstance(msg, AMessage):
            msg = msg.as_dict
        socket.send_json(msg)

# Receiver process.
def receiver(port, recv_queue):
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://127.0.0.1:%d" % port)
    while True:
        msg = socket.recv()
        parsed = yaml.load(msg)
        recv_queue.put(parsed)

send_port = 12355
recv_port = 12356

send_queue = ProcessQueue()
recv_queue = ProcessQueue()

send_process = Process(target=sender, args=(send_port, send_queue))
recv_process = Process(target=receiver, args=(recv_port, recv_queue))
send_process.start()
recv_process.start()

# Sends a message. Not blocking.
def send(msg):
    send_queue.put_nowait(msg)

# Interprets a message and returns an AMessage if it is of AMessage format
def interpret_message(msg):
    # msg is a dictionary
    if msg and msg['header'] and msg['header']['msg_type'] and msg['content']:
        return AMessage(msg['header']['msg_type'], msg['content'])
    else:
        return msg

msg_queues = {}
msg_type_lock = Lock()

# find the correct message queue
def get_msg_queue(msg_type):
    with msg_type_lock: # prevent the creation of two queues
        if msg_type not in msg_queues:
            msg_queues[msg_type] = Queue()
    return msg_queues[msg_type]

# channel processor thread task
# continously interprets and sorts raw messages
def channel_processor():
    while True:
        msg = recv_queue.get()
        msg = interpret_message(msg)
        if isinstance(msg, AMessage):
            channel_queue = get_msg_queue(msg.msg_type)
            channel_queue.put_nowait(msg)

# execute the channel_processor
Thread(target=channel_processor).start()

# Receives a message on a channel. Will block unless you pass block=False.
def recv(channel, block=False):
    msg_queue = get_msg_queue(channel)
    return msg_queue.get(block)
