from daveshed.legobot.inputs import gamepad as controller
from daveshed.adafruit import joint


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
controller.YButtonPressed.handler = grasper.open
controller.YButtonReleased.handler = grasper.close


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

controller.XButtonPressed.handler = handle_x_button_pressed
controller.BButtonPressed.handler = handle_b_button_pressed
controller.LeftDpadPressed.handler = handle_left
controller.RightDpadPressed.handler = handle_right
controller.DownDpadPressed.handler = handle_down
controller.UpDpadPressed.handler = handle_up

reader = controller.GamepadReader(daemon=True)
reader.start()
