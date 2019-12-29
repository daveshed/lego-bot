import controller
import servo


from Adafruit_PCA9685 import PCA9685
from pcaxxx import PcaChannelToServoChannel

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
# from adafruit_motor import servo


import i2c_custom
import pyftdi.i2c
foo = pyftdi.i2c.I2cController()
foo.configure('ftdi:///1')
port = foo.get_port(0x40)
i2c_custom.PORT = port


pca = PCA9685(i2c=i2c_custom)
pca.frequency = 50


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
foo = servo.Servo(PcaChannelToServoChannel(pca, 0))
bar = servo.Servo(PcaChannelToServoChannel(pca, 1))
baz = servo.Servo(PcaChannelToServoChannel(pca, 2))
zed = servo.Servo(PcaChannelToServoChannel(pca, 3))

grasper = Grasper(zed)
controller.LeftButtonClicked.handler = grasper.openclose

sensitivity = -1 / 3.0

def handle_wheel_movement(event):
    baz.angle += event.delta
def handle_x_movement(event):
    foo.angle += event.delta * sensitivity
def handle_y_movement(event):
    bar.angle += event.delta * sensitivity

controller.WheelMoved.handler = handle_wheel_movement
controller.MouseMovedX.handler = handle_x_movement
controller.MouseMovedY.handler = handle_y_movement

reader = controller.MouseReader(daemon=True)
reader.start()

