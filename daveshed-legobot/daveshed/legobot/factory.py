"""
Factory definitions required to start up the application
"""
import inputs

from daveshed.legobot import controller
from daveshed.legobot import robot
from daveshed.legobot.application import AbstractApplicationFactory
from daveshed.legobot.events import gamepad as gamepad_events
from daveshed.legobot.events import mouse as mouse_events
from daveshed.legobot.events import trackpad as trackpad_events
from daveshed.legobot.grasper import LegoServoGrasper

# This import should not be here - concrete factories should be defined in
# the example scripts (entry point) so that we don't have to pollute
# requirements with hardware specific dependencies.
from daveshed.adafruit import joint


class GamepadRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a gamepad.
    """
    # pylint: disable=too-few-public-methods
    def _register_controller(self):
        (
            controller.GamepadController(self.robot)
            .register_handlers(gamepad_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.gamepads[0]

    @staticmethod
    def _get_parser():
        return gamepad_events.GamepadInputEvent.from_raw_input_event

    @staticmethod
    def _make_robot():
        return robot.RobotStub()


class GamepadLegoRobotFactory(AbstractApplicationFactory):
    """
    Factory that creates a lego robot (hardware required) and controls it
    via a gamepad.
    """
    # pylint: disable=too-few-public-methods
    def _register_controller(self):
        (
            controller.GamepadController(self.robot)
            .register_handlers(gamepad_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.gamepads[0]

    @staticmethod
    def _get_parser():
        return gamepad_events.GamepadInputEvent.from_raw_input_event

    @staticmethod
    def _make_robot():
        servos = [
            joint.ServoJointController(channel)
            for channel in joint.PwmChannel.from_channel_numbers((0,1,2,3))
        ]
        grasper = LegoServoGrasper(servos[-1])
        return robot.ThreeDofLegoRobot(joints=servos[0:3], grasper=grasper)


class MouseRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a mouse.
    """
    # pylint: disable=too-few-public-methods
    def _register_controller(self):
        (
            controller.MouseController(self.robot)
                .register_handlers(mouse_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.mice[0]

    @staticmethod
    def _get_parser():
        return mouse_events.MouseInputEvent.from_raw_input_event

    @staticmethod
    def _make_robot():
        return robot.RobotStub()


class MouseLegoRobotFactory(AbstractApplicationFactory):
    """
    Factory that creates a lego robot (hardware required) and controls it
    via a mouse.
    """
    # pylint: disable=too-few-public-methods
    def _register_controller(self):
        controller.MouseController(self.robot).register_handlers(mouse_events)

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.mice[0]

    @staticmethod
    def _get_parser():
        return mouse_events.MouseInputEvent.from_raw_input_event

    @staticmethod
    def _make_robot():
        servos = [
            joint.ServoJointController(channel)
            for channel in joint.PwmChannel.from_channel_numbers((0,1,2,3))
        ]
        grasper = LegoServoGrasper(servos[-1])
        return robot.ThreeDofLegoRobot(joints=servos[0:3], grasper=grasper)


class TrackpadRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a trackpad device.
    """
    # pylint: disable=too-few-public-methods
    def _register_controller(self):
        (
            controller.TrackpadController(self.robot)
                .register_handlers(trackpad_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.mice[0]

    @staticmethod
    def _get_parser():
        return trackpad_events.TrackpadInputEvent.from_raw_input_event

    @staticmethod
    def _make_robot():
        return robot.RobotStub()


class TrackpadLegoRobotFactory(AbstractApplicationFactory):
    """
    Factory that creates a lego robot (hardware required) and controls it
    via a trackpad device.
    """
    # pylint: disable=too-few-public-methods
    def _register_controller(self):
        (
            controller.TrackpadController(self.robot)
                .register_handlers(trackpad_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.mice[0]

    @staticmethod
    def _get_parser():
        return trackpad_events.TrackpadInputEvent.from_raw_input_event

    @staticmethod
    def _make_robot():
        servos = [
            joint.ServoJointController(channel)
            for channel in joint.PwmChannel.from_channel_numbers((0,1,2,3))
        ]
        grasper = LegoServoGrasper(servos[-1])
        return robot.ThreeDofLegoRobot(joints=servos[0:3], grasper=grasper)
