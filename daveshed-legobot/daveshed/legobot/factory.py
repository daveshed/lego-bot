"""
Factory definitions required to start up the application
"""
import inputs

from daveshed.legobot import controller
from daveshed.legobot.application import AbstractApplicationFactory
from daveshed.legobot.events import gamepad as gamepad_events
from daveshed.legobot.events import mouse as mouse_events
from daveshed.legobot.events import trackpad as trackpad_events
from daveshed.legobot.robot import RobotStub


class GamepadRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a gamepad.
    """
    # pylint: disable=too-few-public-methods
    @staticmethod
    def _register_controller():
        (
            controller.GamepadController(RobotStub())
                .register_handlers(gamepad_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.gamepads[0]

    @staticmethod
    def _get_parser():
        return gamepad_events.GamepadInputEvent.from_raw_input_event


class MouseRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a mouse.
    """
    # pylint: disable=too-few-public-methods
    @staticmethod
    def _register_controller():
        (
            controller.MouseController(RobotStub())
                .register_handlers(mouse_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.mice[0]

    @staticmethod
    def _get_parser():
        return mouse_events.MouseInputEvent.from_raw_input_event


class TrackpadRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a trackpad device.
    """
    # pylint: disable=too-few-public-methods
    @staticmethod
    def _register_controller():
        (
            controller.TrackpadController(RobotStub())
                .register_handlers(trackpad_events)
        )

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.mice[0]

    @staticmethod
    def _get_parser():
        return trackpad_events.TrackpadInputEvent.from_raw_input_event
