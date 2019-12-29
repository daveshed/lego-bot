# from Adafruit_PCA9685 import PCA9685
# from pcaxxx import PcaChannelToServoChannel

# # This example also relies on the Adafruit motor library available here:
# # https://github.com/adafruit/Adafruit_CircuitPython_Motor
# # from adafruit_motor import servo


# import i2c_custom
# import pyftdi.i2c
# foo = pyftdi.i2c.I2cController()
# foo.configure('ftdi:///1')
# port = foo.get_port(0x40)
# i2c_custom.PORT = port


# pca = PCA9685(i2c=i2c_custom)
# pca.frequency = 50

class Servo:
    MIN_ANGLE_DEG = 0.0
    MIN_DUTY_CYCLE = 0.0025
    MAX_ANGLE_DEG = 180.0
    MAX_DUTY_CYCLE = 0.5

    def __init__(self, channel):
        self._channel = channel
        self.angle = 90

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, deg):
        self._channel.set_duty_cycle(self._get_duty_cycle(deg))
        self._angle = deg

    @classmethod
    def _get_duty_cycle(cls, deg):
        m = (cls.MAX_DUTY_CYCLE - cls.MIN_DUTY_CYCLE) / (cls.MAX_ANGLE_DEG - cls.MIN_ANGLE_DEG)
        c = cls.MIN_DUTY_CYCLE
        result = (m * deg) + c
        print("duty cycle %f" % result)
        return result


# foo = Servo(PcaChannelToServoChannel(pca, 0))
# bar = Servo(PcaChannelToServoChannel(pca, 1))
# baz = Servo(PcaChannelToServoChannel(pca, 2))
# zed = Servo(PcaChannelToServoChannel(pca, 3))


