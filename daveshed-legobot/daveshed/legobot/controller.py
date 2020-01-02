import logging

_LOGGER = logging.getLogger("CONTROLLER")


class RobotControllerBase:
    """
    Base-class for a robot controller. This defines the API required by the
    robot to understand the commands from a controller / human input device such
    as a trackpad, gamepad or mouse. Input events from the human input device
    will be mapped to method calls here.
    """
    def __init__(self, robot):
        self._robot = robot
        self.position = None

    @property
    def robot(self):
        return self._robot

    def handle_relative_x(self, value):
        self.robot.move_x(rate=value)

    def handle_relative_y(self, value):
        self.robot.move_y(rate=value)

    def handle_relative_z(self, value):
        self.robot.move_z(rate=value)

    def handle_absolute_x(self, value):
        _XUpdate(self, value).execute()

    def handle_absolute_y(self, value):
        _YUpdate(self, value).execute()

    def handle_absolute_z(self, value):
        _ZUpdate(self, value).execute()

    def handle_absolute_start(self):
        _LOGGER.debug("Starting absolute movement")
        self.position = _AbsolutePositionValues()

    def handle_absolute_complete(self):
        _LOGGER.debug("Absolute movement complete")
        self.robot.stop()
        self.position = None

    def register_handlers(self, events):
        raise NotImplementedError


class TrackpadController(RobotControllerBase):

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
            lambda event: self.handle_absolute_x(event.position))
        events.TrackpadMovedY.register_handler(
            lambda event: self.handle_absolute_y(event.position))

    def _deregister_xy_movement_handlers(self, events):
        events.TrackpadMovedX.deregister_handler()
        events.TrackpadMovedY.deregister_handler()

    def _register_z_movement_handlers(self, events):
        # since only one trackpad is available that has two degrees of freedom,
        # we need to change mode using the right button to enable z movment mode
        events.TrackpadMovedY.register_handler(
            lambda event: self.handle_absolute_z(event.position))

    def _deregister_z_movement_handlers(self, events):
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

    def __init__(self, controller):
        if controller.position is None:
            raise RuntimeError(
                "Cannot update absolute position without start notification")

    def execute(self):
        _LOGGER.debug("Updating position")
        if self._get_position() is None:
            pass
        else:
            delta = self._new_position - self._get_position()
            self._move_robot(rate=delta)
        self._set_position(self._new_position)


class _XUpdate(_AbsolutePositionUpdate):

    def __init__(self, controller, x_new):
        super().__init__(controller)
        self._new_position = x_new
        self._get_position = controller.position.get_x
        self._set_position = controller.position.set_x
        self._move_robot = controller.robot.move_x


class _YUpdate(_AbsolutePositionUpdate):

    def __init__(self, controller, y_new):
        super().__init__(controller)
        self._new_position = y_new
        self._get_position = controller.position.get_y
        self._set_position = controller.position.set_y
        self._move_robot = controller.robot.move_y


class _ZUpdate(_AbsolutePositionUpdate):

    def __init__(self, controller, z_new):
        super().__init__(controller)
        self._new_position = z_new
        self._get_position = controller.position.get_z
        self._set_position = controller.position.set_z
        self._move_robot = controller.robot.move_z
