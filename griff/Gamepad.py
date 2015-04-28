import soothsayer
import pykka

axes = [0]
buttons = [0]

class GamepadStateUpdater(pykka.ThreadingActor):

    def __init__(self):
        super(GamepadStateUpdater, self).__init__()
        self.axes = [0]
        self.buttons = [0]

    def on_receive(self, message):
        print 'got message'
        print message
        self.axes = message.axes
        self.buttons = message.buttons

gsu = GamepadStateUpdater.start()
gsup = gsu.proxy()

soothsayer.on('gamepad', gsu)

def axes():
    gsup.axes.get()

def buttons():
    gsup.buttons.get()
