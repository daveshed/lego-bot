"""
Robot controller definitions that interpret events from human interface devices
and map them to commands applied to a robot.
"""
import logging

_LOGGER = logging.getLogger("CONTROLLER")


class RobotControllerBase:
    """
    Base-class for a robot controller. This defines the API required by the
    robot to understand the commands from a controller/human input device such
    as a trackpad, gamepad or mouse. Input events from the human input device
    will be mapped to method calls here.

    Args:
        robot (daveshed.legobot.robot.Robot): a robot that will be controlled
    """
    def __init__(self, robot):
        self._robot = robot
        self.position = None

    @property
    def robot(self):
        """
        The robot object under control

        Returns:
            daveshed.legobot.robot.Robot: the robot object
        """
        return self._robot

    def handle_relative_position(self, axis, value):
        """
        Handle a relative change in the controller's relative position. This
        value will be mapped to the robot's movement in the axis specified.

        Args:
            axis (str): the axis in which to map the movement
            value (float): the relative change read from the controller which
                will be mapped to the robot's speed of movement
        """
        {
            "X": self.robot.move_x,
            "Y": self.robot.move_y,
            "Z": self.robot.move_z,
        }[axis](value)

    def handle_absolute_position(self, axis, value):
        """
        Handle an absolute change in controller absolute position. This value
        will be mapped to the robot's movement in the specified axis. Note that
        the controller's starting position will be recorded and the magnitude of
        its change in position will be used to determine the rate at which the
        robot should move in response.

        Args:
            axis (str): the axis in which to map the movement
            value (float): the updated absolute position of the controller
        """
        if self.position is None:
            raise RuntimeError(
                "Cannot update absolute position without start notification")
        updater = _AbsolutePositionUpdate.from_axis_specifier(axis)
        updater(self, value).execute()

    def handle_absolute_start(self):
        """
        Notify the controller that an absolute position update has begun.
        """
        _LOGGER.debug("Starting absolute movement")
        self.position = _AbsolutePositionValues()

    def handle_absolute_complete(self):
        """
        Notify the controller that the absolute position update that it is
        handling has completed.
        """
        _LOGGER.debug("Absolute movement complete")
        self.position = None

    def register_handlers(self, events):
        """
        Register handlers for all relevant user interface device events.

        Args:
            events (module): Event definitions relevant to a given piece of
                hardware such as a trackpad
        """
        raise NotImplementedError


class GamepadController(RobotControllerBase):
    """
    A concrete implementation of a `RobotControllerBase` class. It maps events
    from a gamepad to robot commands.
    """
    def register_handlers(self, events):
        _LOGGER.debug("Registering handlers for %r", events)
        self._register_for_xy_movements(events)
        self._register_for_z_movements(events)
        self._register_grasper_handlers(events)

    def _register_for_xy_movements(self, events):
        events.UpDpadPressed.register_handler(
            lambda _: self.handle_relative_position("Y", 1))
        events.DownDpadPressed.register_handler(
            lambda _: self.handle_relative_position("Y", -1))
        events.LeftDpadPressed.register_handler(
            lambda _: self.handle_relative_position("X", -1))
        events.RightDpadPressed.register_handler(
            lambda _: self.handle_relative_position("X", 1))

    def _register_for_z_movements(self, events):
        events.XButtonPressed.register_handler(
            lambda _: self.handle_relative_position("Z", 1))
        events.BButtonPressed.register_handler(
            lambda _: self.handle_relative_position("Z", -1))

    def _register_grasper_handlers(self, events):
        events.YButtonPressed.register_handler(
            lambda _: self.robot.open_grasper())
        events.YButtonReleased.register_handler(
            lambda _: self.robot.close_grasper())


class MouseController(RobotControllerBase):
    """
    A concrete implementation of a `RobotControllerBase` class. It maps events
    from a mouse to robot commands.
    """
    def register_handlers(self, events):
        _LOGGER.debug("Registering handlers for %r", events)
        self._register_for_relative_movements(events)
        self._register_grasper_handlers(events)

    def _register_for_relative_movements(self, events):
        events.MouseMovedX.register_handler(
            lambda event: self.handle_relative_position("X", event.delta))
        events.MouseMovedY.register_handler(
            lambda event: self.handle_relative_position("Y", event.delta))
        events.WheelMoved.register_handler(
            lambda event: self.handle_relative_position("Z", event.delta))

    def _register_grasper_handlers(self, events):
        events.LeftButtonClicked.register_handler(
            lambda _: self.robot.open_grasper())
        events.LeftButtonReleased.register_handler(
            lambda _: self.robot.close_grasper())


class TrackpadController(RobotControllerBase):
    """
    A concrete implementation of a `RobotControllerBase` class. It maps events
    from a trackpad device to the robot.
    """
    def register_handlers(self, events):
        _LOGGER.debug("Registering handlers for %r", events)
        self._register_for_absolute_movements(events)
        self._register_movement_mode_handlers(events)
        self._register_grasper_handlers(events)
        self._set_xy_movement_mode(events)

    def _set_xy_movement_mode(self, events):
        self._deregister_z_movement_handlers(events)
        self._register_xy_movement_handlers(events)

    def _set_z_movement_mode(self, events):
        self._deregister_xy_movement_handlers(events)
        self._register_z_movement_handlers(events)

    def _register_for_absolute_movements(self, events):
        # trackpads emit absolute position updates after a button touch event
        # which are followed by another button touch event when the user takes
        # their finger of the device.
        events.PadTouched.register_handler(
            lambda _: self.handle_absolute_start())
        events.PadReleased.register_handler(
            lambda _: self.handle_absolute_complete())

    def _register_xy_movement_handlers(self, events):
        events.TrackpadMovedX.register_handler(
            lambda event: self.handle_absolute_position("X", event.position))
        events.TrackpadMovedY.register_handler(
            lambda event: self.handle_absolute_position("Y", event.position))

    @staticmethod
    def _deregister_xy_movement_handlers(events):
        events.TrackpadMovedX.deregister_handler()
        events.TrackpadMovedY.deregister_handler()

    def _register_z_movement_handlers(self, events):
        # since only one trackpad is available that has two degrees of freedom,
        # we need to change mode using the right button to enable z movment mode
        events.TrackpadMovedY.register_handler(
            lambda event: self.handle_absolute_position("Z", event.position))

    @staticmethod
    def _deregister_z_movement_handlers(events):
        events.TrackpadMovedY.deregister_handler()

    def _register_grasper_handlers(self, events):
        events.LeftButtonClicked.register_handler(
            lambda _: self.robot.open_grasper())
        events.LeftButtonReleased.register_handler(
            lambda _: self.robot.close_grasper())

    def _register_movement_mode_handlers(self, events):
        events.RightButtonClicked.register_handler(
            lambda _: self._set_z_movement_mode(events))
        events.RightButtonReleased.register_handler(
            lambda _: self._set_xy_movement_mode(events))


class _AbsolutePositionValues:
    # pylint: disable=missing-docstring
    def __init__(self):
        self._x = None
        self._y = None
        self._z = None

    def set_x(self, value):
        self._x = value

    def get_x(self):
        return self._x

    def set_y(self, value):
        self._y = value

    def get_y(self):
        return self._y

    def set_z(self, value):
        self._z = value

    def get_z(self):
        return self._z


class _AbsolutePositionUpdate:
    # pylint: disable=missing-docstring

    @staticmethod
    def from_axis_specifier(axis):
        return {
            "X": _XUpdate,
            "Y": _YUpdate,
            "Z": _ZUpdate,
        }[axis]

    def execute(self):
        _LOGGER.debug("Updating position")
        # getters/setters will be specified in the init of each command.
        # pylint: disable=no-member
        if self._get_position() is None:
            pass
        else:
            delta = self._new_position - self._get_position()
            self._move_robot(delta)
        self._set_position(self._new_position)


class _XUpdate(_AbsolutePositionUpdate):
    # pylint: disable=missing-docstring
    def __init__(self, controller, x_new):
        self._new_position = x_new
        self._get_position = controller.position.get_x
        self._set_position = controller.position.set_x
        self._move_robot = controller.robot.move_x


class _YUpdate(_AbsolutePositionUpdate):
    # pylint: disable=missing-docstring
    def __init__(self, controller, y_new):
        self._new_position = y_new
        self._get_position = controller.position.get_y
        self._set_position = controller.position.set_y
        self._move_robot = controller.robot.move_y


class _ZUpdate(_AbsolutePositionUpdate):
    # pylint: disable=missing-docstring
    def __init__(self, controller, z_new):
        self._new_position = z_new
        self._get_position = controller.position.get_z
        self._set_position = controller.position.set_z
        self._move_robot = controller.robot.move_z
