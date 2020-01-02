import unittest
from unittest import mock

from daveshed.legobot import controller
from daveshed.legobot.robot import Robot


class ControllerTestGroup(unittest.TestCase):

    def setUp(self):
        self.robot = mock.Mock(name="Robot", spec_set=Robot)
        self.controller = controller.ControllerBase(self.robot)

    def test_relative_movement_moves_robot(self):
        self.controller.handle_relative_x(2)
        self.robot.move_x.assert_called_with(rate=2)
        self.controller.handle_relative_y(1.3)
        self.robot.move_y.assert_called_with(rate=1.3)
        self.controller.handle_relative_z(-45)
        self.robot.move_z.assert_called_with(rate=-45)

    def test_absolute_x_movement_moves_x_interprets_rate(self):
        self.controller.handle_absolute_start()
        self.controller.handle_absolute_x(2.3)
        self.controller.handle_absolute_x(3.3)
        self.controller.handle_absolute_complete()
        self.robot.move_x.assert_called_with(rate=3.3 - 2.3)
        self.robot.move_y.assert_not_called()
        self.robot.move_z.assert_not_called()
        self.robot.stop.assert_called_once()

    def test_absolute_y_movement_moves_y_interprets_rate(self):
        self.controller.handle_absolute_start()
        self.controller.handle_absolute_y(-4.6)
        self.controller.handle_absolute_y(1.09)
        self.controller.handle_absolute_complete()
        self.robot.move_x.assert_not_called()
        self.robot.move_y.assert_called_with(rate=1.09 - -4.6)
        self.robot.move_z.assert_not_called()
        self.robot.stop.assert_called_once()

    def test_absolute_z_movement_moves_z_interprets_rate(self):
        self.controller.handle_absolute_start()
        self.controller.handle_absolute_z(0.0)
        self.controller.handle_absolute_z(3.3)
        self.controller.handle_absolute_complete()
        self.robot.move_x.assert_not_called()
        self.robot.move_y.assert_not_called()
        self.robot.move_z.assert_called_with(rate=3.3 - 0.0)
        self.robot.stop.assert_called_once()
