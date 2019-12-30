import abc


class JointControllerBase(abc.ABC):
    """
    A robot joint controller base class that must be implemented in order to
    use a robot. It defines the interface required by the robot of each joint
    and forces dependency inversion of the low-level joint controller
    implementations ie. the robot will not depend on low-level libraries rather
    joint controller implementations will depend on the robot library.
    """

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
