import soothsayer

axes = [0]
buttons = [0]

def update_vars(msg):
    global axes
    global buttons
    axes = msg.content['axes']
    buttons = msg.content['buttons']

soothsayer.on('gamepad', update_vars)
