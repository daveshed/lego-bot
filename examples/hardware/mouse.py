import logging

from daveshed.legobot.inputs import mouse as controller
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

def handle_wheel_movement(event):
    baz.angle += event.delta
def handle_x_movement(event):
    foo.angle -= event.delta
def handle_y_movement(event):
    bar.angle -= event.delta

controller.WheelMoved.register_handler(handle_wheel_movement)
controller.MouseMovedX.register_handler(handle_x_movement)
controller.MouseMovedY.register_handler(handle_y_movement)

from daveshed.legobot.inputs.base import UserInputEventConsumer
from daveshed.legobot.inputs.mouse import MouseInputEvent
import inputs

mouse = inputs.devices.mice[0]

reader = UserInputEventConsumer(
    device=mouse,
    event_type=MouseInputEvent,
    daemon=True)
reader.start()

