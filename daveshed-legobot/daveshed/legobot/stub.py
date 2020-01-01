import logging

from daveshed.legobot.joint import JointControllerBase

_LOGGER = logging.getLogger("JOINT")


class FakeJointController(JointControllerBase):
    """
    A stub for the joint controller useful for testing and development without
    any physical hardware connected.
    """
    def __init__(self, angle, idx):
        self._home_position = angle
        self._angle = angle
        self._idx = idx
        _LOGGER.info("Instantiating joint <%r>", self._idx)

    def home(self):
        _LOGGER.info("Homing joint <%r> -> %r", self._idx, self._angle)
        self.angle = self._home_position

    @property
    def speed(self):
        # TODO...
        raise NotImplementedError

    def _set_speed(self, value):
        # TODO...
        raise NotImplementedError

    def _set_angle(self, angle):
        _LOGGER.info("Setting joint <%r> -> %r", self._idx, self._angle)
        self._angle = angle
