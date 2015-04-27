import zmq, yaml
from multiprocessing import Process, Queue
from Queue import Empty

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

send_queue = None
recv_queue = None

# Doesn't do anything.
def init():
    pass

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

# Receives a message, or None if there is no current message.
# If block is True, blocks.
def recv(block=False):
    if block:
        msg = recv_queue.get()
        return interpret_message(msg)
    else:
        try:
            msg = recv_queue.get_nowait()
            return interpret_message(msg)
        except Empty:
            return None

# Intialize on module import
send_port = 12355
recv_port = 12356

send_queue = Queue()
recv_queue = Queue()

send_process = Process(target=sender, args=(send_port, send_queue))
recv_process = Process(target=receiver, args=(recv_port, recv_queue))
send_process.start()
recv_process.start()
