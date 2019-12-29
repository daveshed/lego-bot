class PcaChannelToServoChannel:
    RESOLUTION = 4096

    def __init__(self, pca, channel):
        self._pca = pca
        self._channel = channel

    def set_duty_cycle(self, value):
        """
        Input the duty cycle as a ratio
        """
        assert value > 0.0, "Cannot set negative duty cycle"
        off_time = int(value * self.RESOLUTION)
        print("Setting off time to %d" % off_time)
        self._pca.set_pwm(self._channel, 0, off_time)


