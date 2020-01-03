"""
Joint controller definitions. A base class is available here to enforce
dependency inversion - lower-level libraries may then implement this base class
so that the robot library may be ignorant of joint controller implementation.
"""
import abc
import logging

_LOGGER = logging.getLogger("JOINT")


class JointControllerBase(abc.ABC):
    """
    A robot joint controller base class that must be implemented in order to
    use a robot. It defines the interface required by the robot of each joint
    and forces dependency inversion of the low-level joint controller
    implementations ie. the robot will not depend on low-level libraries rather
    joint controller implementations will depend on the robot library.
    """
    def __init__(self, angle):
        self._angle = angle

    @property
    def angle(self):
        """
        The current angle of the joint at the moment in degrees measured from
        the datum angle.

        Returns:
            float: the angle
        """
        return self._angle

    @angle.setter
    def angle(self, angle):
        """
        Set the angle of the joint in degrees from the datum

        Args:
            angle (float): the angle to set
        """
        self._set_angle(angle)

    @abc.abstractmethod
    def _set_angle(self, angle):
        """
        Private implementation required to set the joint angle

        Args:
            angle (float): the angle to set
        """

    @abc.abstractmethod
    def home(self):
        """
        Return the joint to its home position
        """

    @property
    @abc.abstractmethod
    def speed(self):
        """
        The rotation speed of the joint in degrees / second

        Returns:
            float: the rotation speed in degrees / sec
        """

    @speed.setter
    def speed(self, value):
        """
        Sets the rotation speed of the joint in degrees / second

        Args:
            value (float): the rotation speed in degrees / sec
        """
        self._set_speed(value)

    @abc.abstractmethod
    def _set_speed(self, value):
        """
        Private implementation required to set the joint angle

        Args:
            angle (float): the angle to set
        """


class FakeJointController(JointControllerBase):
    """
    A stub for the joint controller useful for testing and development without
    any physical hardware connected.
    """
    def __init__(self, angle, idx):
        super().__init__(angle)
        self._home_position = angle
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
