import abc


class Robot(abc.ABC):
    """
    The robot base-class has a fixed API that will be accessed by a controller
    object or alternatively by direct calls.
    """

    @abc.abstractmethod
    def move_x(self, rate):
        """
        Respond to a movement command in the x-axis at the specified rate

        Args:
            rate (float): the rate at which to move in the x direction in units
                per second.
        """

    @abc.abstractmethod
    def move_y(self, rate):
        """
        Respond to a movement command in the y-axis at the specified rate

        Args:
            rate (float): the rate at which to move in the y direction in units
                per second.
        """

    @abc.abstractmethod
    def move_z(self, rate):
        """
        Respond to a movement command in the z-axis at the specified rate

        Args:
            rate (float): the rate at which to move in the x direction in units
                per second.
        """

    @abc.abstractmethod
    def stop(self):
        """
        Stop moving following a move command.
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
