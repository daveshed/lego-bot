
class ControllerBase:
    """
    Base-class for a robot controller. This defines the API required by the
    robot to understand the commands from a controller / human input device such
    as a trackpad, gamepad or mouse. Input events from the human input device
    will be mapped to method calls here.
    """
    def __init__(self, robot):
        self._rate = 0
        self._robot = robot
        self.position = _AbsolutePositionValues()

    @property
    def robot(self):
        return self._robot

    def handle_relative_x(self, value):
        self._robot.move_x(rate=value)

    def handle_relative_y(self, value):
        self._robot.move_y(rate=value)

    def handle_relative_z(self, value):
        self._robot.move_z(rate=value)

    def handle_absolute_x(self, value):
        _XUpdate(self, value).execute()

    def handle_absolute_y(self, value):
        _YUpdate(self, value).execute()

    def handle_absolute_z(self, value):
        _ZUpdate(self, value).execute()

    def handle_absolute_start(self):
        self.position = _AbsolutePositionValues()

    def handle_absolute_complete(self):
        self._robot.stop()


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

    def execute(self):
        if self._get_position() is None:
            pass
        else:
            delta = self._new_position - self._get_position()
            self._move_robot(rate=delta)
        self._set_position(self._new_position)


class _XUpdate(_AbsolutePositionUpdate):

    def __init__(self, controller, x_new):
        self._new_position = x_new
        self._get_position = controller.position.get_x
        self._set_position = controller.position.set_x
        self._move_robot = controller.robot.move_x


class _YUpdate(_AbsolutePositionUpdate):

    def __init__(self, controller, y_new):
        self._new_position = y_new
        self._get_position = controller.position.get_y
        self._set_position = controller.position.set_y
        self._move_robot = controller.robot.move_y


class _ZUpdate(_AbsolutePositionUpdate):

    def __init__(self, controller, z_new):
        self._new_position = z_new
        self._get_position = controller.position.get_z
        self._set_position = controller.position.set_z
        self._move_robot = controller.robot.move_z
