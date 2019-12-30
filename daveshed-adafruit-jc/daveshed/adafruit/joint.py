import logging

import Adafruit_PCA9685

from daveshed.adafruit import i2c as i2c_interface
from daveshed.legobot.joint import JointControllerBase

_LOGGER = logging.getLogger("JOINT")


class PwmChannel:
    """
    Implementation of PWM channel provided by the F232H and PCA9685 hardware
    set.

    Args:
        pca (Adafruit_PCA9685.PCA9685): pulse width modulation device
        channel (int): the channel to drive
    """
    RESOLUTION = 4096
    def __init__(self, pca, channel):
        self._pca = pca
        self._channel = channel
        self._duty_cycle = None

    @property
    def duty_cycle(self):
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        assert value > 0.0, "Cannot set negative duty cycle"
        off_time = int(value * self.RESOLUTION)
        self._pca.set_pwm(self._channel, 0, off_time)

    @classmethod
    def from_channel_numbers(cls, channels):
        pca = Adafruit_PCA9685.PCA9685(i2c=i2c_interface)
        pca.frequency = 50
        return (cls(pca, idx) for idx in channels)


class ServoJointController(JointControllerBase):
    """
    A servo controller.

    Args:
        channel (PwmChannelBase): the channel that should be used to control the
            servo through pulse-width-modulation.
    """
    MIN_ANGLE_DEG = 0.0
    MIN_DUTY_CYCLE = 0.0025
    MAX_ANGLE_DEG = 180.0
    MAX_DUTY_CYCLE = 0.5
    INITIAL_ANGLE_DEG = 90

    def __init__(self, channel: PwmChannel):
        self._channel = channel
        self._angle = None
        self.angle = self.INITIAL_ANGLE_DEG

    def _set_angle(self, angle):
        self._channel.duty_cycle = self._get_duty_cycle(angle)
        _LOGGER.info("Setting angle to %f", angle)
        self._angle = angle

    def home(self):
        # FIXME
        pass

    def _set_speed(self, value):
        # FIXME
        pass

    @property
    def speed(self):
        # FIXME
        return None

    @classmethod
    def _get_duty_cycle(cls, deg):
        m = (
            (cls.MAX_DUTY_CYCLE - cls.MIN_DUTY_CYCLE)
            / (cls.MAX_ANGLE_DEG - cls.MIN_ANGLE_DEG)
        )
        c = cls.MIN_DUTY_CYCLE
        return (m * deg) + c
