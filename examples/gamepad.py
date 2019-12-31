import logging

from daveshed.legobot.inputs import gamepad as controller
from daveshed.adafruit import joint

logging.basicConfig(level=logging.INFO)


class Grasper:
    OPEN_ANGLE = 65
    CLOSED_ANGLE = 90

    def __init__(self, servo):
        self._servo = servo
        self._open = None
        self.open()

    def openclose(self):
        if self._open:
            self.close()
        else:
            self.open()

    def open(self):
        print("OPENING...")
        self._servo.angle = self.OPEN_ANGLE
        # race condition?
        self._open = True

    def close(self):
        print("CLOSING...")
        self._servo.angle = self.CLOSED_ANGLE
        # race condition?
        self._open = False


# FIXME: define a robot object...
foo, bar, baz, zed = (
    joint.ServoJointController(channel)
    for channel in joint.PwmChannel.from_channel_numbers((0,1,2,3,))
)

grasper = Grasper(zed)

def handle_y_button_pressed(event):
    grasper.open()
def handle_y_button_released(event):
    grasper.close()
def handle_x_button_pressed(event):
    baz.angle += 1
def handle_b_button_pressed(event):
    baz.angle -= 1
def handle_left(event):
    foo.angle += 1
def handle_right(event):
    foo.angle -= 1
def handle_up(event):
    bar.angle += 1
def handle_down(event):
    bar.angle -= 1

controller.YButtonPressed.register_handler(handle_y_button_pressed)
controller.YButtonReleased.register_handler(handle_y_button_released)
controller.XButtonPressed.register_handler(handle_x_button_pressed)
controller.BButtonPressed.register_handler(handle_b_button_pressed)
controller.LeftDpadPressed.register_handler(handle_left)
controller.RightDpadPressed.register_handler(handle_right)
controller.DownDpadPressed.register_handler(handle_down)
controller.UpDpadPressed.register_handler(handle_up)

from daveshed.legobot.inputs.base import UserInputEventConsumer
from daveshed.legobot.inputs.gamepad import GamepadInputEvent
import inputs

pad = inputs.devices.gamepads[0]

reader = UserInputEventConsumer(
    device=pad,
    event_type=GamepadInputEvent,
    daemon=True)
reader.start()
