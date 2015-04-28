import soothsayer

axes = [0]
buttons = [0]

def update(msg):
    axes[0] = msg.content['axes'][0]
    buttons = msg.content['buttons']

soothsayer.on('gamepad', update)

