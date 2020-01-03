"""
A concrete implementation of the joint controller interface defined by the the
legobot.
"""
import logging
import time

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
        """
        The duty cycle of the pwm output

        Returns:
            float: the duty cycle
        """
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        """
        Sets the duty cycle of pwm output.

        Args:
            value (float): the duty cycle between 0 and 1
        """
        assert value > 0.0, "Cannot set negative duty cycle"
        assert value <= 1.0, "Cannot set duty cycle larger than 1"
        off_time = int(value * self.RESOLUTION)
        self._pca.set_pwm(self._channel, 0, off_time)

    @classmethod
    def from_channel_numbers(cls, channels):
        """
        A factory method to create pwm channels from an iterable of channel
        numbers

        Args:
            iterable of ints: the index of each channel to create a pwm channel
                on.
        """
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
    _SLOPE = (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) / (MAX_ANGLE_DEG - MIN_ANGLE_DEG)
    _INTERCEPT = MIN_DUTY_CYCLE

    def __init__(self, channel: PwmChannel):
        super().__init__(None)
        self._channel = channel
        self.angle = self.INITIAL_ANGLE_DEG

    def _set_angle(self, angle):
        self._channel.duty_cycle = self._get_duty_cycle(angle)
        _LOGGER.info("Setting angle to %f", angle)
        self._angle = angle

    def home(self):
        delta = self.INITIAL_ANGLE_DEG - self.angle
        if delta == 0.0:
            return
        stride = delta / abs(delta)
        for angle in range(
                round(self.angle),
                round(self.INITIAL_ANGLE_DEG),
                round(stride)):
            self.angle = angle
            time.sleep(0.02)

    @classmethod
    def _get_duty_cycle(cls, deg):
        return (cls._SLOPE * deg) + cls._INTERCEPT
