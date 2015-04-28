import ansible
axes = [0.0] * 4
buttons = [0.0] * 17

# thread that runs to update the gamepad state
def update_thread():
    global axes
    global buttons
    while True:
        msg = ansible.recv('gamepad')
        axes = msg.content['axes']
        buttons = msg.content['buttons']
