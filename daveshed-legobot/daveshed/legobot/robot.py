"""
Robot class definitions
"""
import abc
import logging

_LOGGER = logging.getLogger("ROBOT")


class Robot(abc.ABC):
    """
    The robot base-class has a fixed API that will be accessed by a controller
    object or alternatively by direct calls.
    """

    @abc.abstractmethod
    def move_x(self, distance):
        """
        Respond to a movement command in the x-axis over the specified distance

        Args:
            distance (float): the distance to move
        """

    @abc.abstractmethod
    def move_y(self, distance):
        """
        Respond to a movement command in the y-axis over the specified distance

        Args:
            distance (float): the distance to move
        """

    @abc.abstractmethod
    def move_z(self, distance):
        """
        Respond to a movement command in the y-axis over the specified distance

        Args:
            distance (float): the distance to move
        """

    @abc.abstractmethod
    def open_grasper(self):
        """
        Open the grasper
        """

    @abc.abstractmethod
    def close_grasper(self):
        """
        Close the grasper
        """

    @abc.abstractmethod
    def home(self):
        """
        Return the robot to its home position
        """

    @abc.abstractmethod
    def enable(self):
        """
        Enable control of the robot so that it responds to instructions to move
        and open/close the grasper etc.
        """

    @abc.abstractmethod
    def disable(self):
        """
        Disable control of the robot so that it will not respond to instructions
        to instructions to move or open/close the grasper etc.
        """


class RobotStub(Robot):
    """
    A stubbed robot implementation that simply logs method calls using the
    python logger.
    """
    def move_x(self, distance):
        _LOGGER.info("Moving %r in x...", distance)

    def move_y(self, distance):
        _LOGGER.info("Moving %r in y...", distance)

    def move_z(self, distance):
        _LOGGER.info("Moving %r in z...", distance)

    def stop(self):
        _LOGGER.info("Stop moving")

    def open_grasper(self):
        _LOGGER.info("Opening grasper...")

    def close_grasper(self):
        _LOGGER.info("Closing grasper...")

    def home(self):
        _LOGGER.info("Homing...")

    def enable(self):
        _LOGGER.info("Enabled")

    def disable(self):
        _LOGGER.info("Disabled")


class ThreeDofLegoRobot(Robot):
    """
    A simple lego robot implementation that has three joints and a grasper.

    Args:
        joints (tuple): `JointController`s corresponding to the robot's joints
        grasper (daveshed.legobot.grasper.Grasper): a grasper to be part of the
            robot
    """
    def __init__(self, joints, grasper):
        self._joints = joints
        self._grasper = grasper
        self.home()

    def move_x(self, distance):
        _LOGGER.info("Moving %r in x...", distance)
        self._joints[0].angle += distance

    def move_y(self, distance):
        _LOGGER.info("Moving %r in y...", distance)
        self._joints[1].angle += distance

    def move_z(self, distance):
        _LOGGER.info("Moving %r in z...", distance)
        self._joints[2].angle += distance

    def open_grasper(self):
        _LOGGER.info("Opening grasper...")
        self._grasper.open()

    def close_grasper(self):
        _LOGGER.info("Closing grasper...")
        self._grasper.close()

    def home(self):
        _LOGGER.info("Homing...")
        for joint in self._joints:
            joint.home()

    def enable(self):
        _LOGGER.info("Enabled")
        # FIXME: requires states

    def disable(self):
        _LOGGER.info("Disabled")
        # FIXME: requires states
