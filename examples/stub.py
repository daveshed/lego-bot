import logging

from daveshed.legobot.inputs import trackpad as controller
from daveshed.legobot import stub

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
    stub.FakeJointController(angle=0.0, idx=idx)
    for idx in range(4)
)

grasper = Grasper(zed)

def handle_x_movement(event):
    foo.angle = event.position
def handle_y_movement(event):
    bar.angle = event.position
def handle_mouse_clicked(event):
    grasper.close()
def handle_mouse_released(event):
    grasper.open()

controller.TrackpadMovedX.register_handler(handle_x_movement)
controller.TrackpadMovedY.register_handler(handle_y_movement)
controller.LeftButtonClicked.register_handler(handle_mouse_clicked)
controller.LeftButtonReleased.register_handler(handle_mouse_released)

from daveshed.legobot.inputs.base import UserInputEventConsumer
from daveshed.legobot.inputs.trackpad import TrackpadInputEvent
import inputs

mouse = inputs.devices.mice[0]

reader = UserInputEventConsumer(
    device=mouse,
    event_type=TrackpadInputEvent,
    daemon=True)
reader.start()

