"""
Factory definitions required to start up the application
"""
import inputs

from daveshed.legobot.application import AbstractApplicationFactory
from daveshed.legobot.controller import GamepadController
from daveshed.legobot.events import gamepad as gamepad_events
from daveshed.legobot.robot import RobotStub


class GamepadRobotStubFactory(AbstractApplicationFactory):
    """
    Factory that creates a robot stub (no hardware required) and controls it
    via a gamepad.
    """
    # pylint: disable=too-few-public-methods
    @staticmethod
    def _register_controller():
        GamepadController(RobotStub()).register_handlers(gamepad_events)

    @staticmethod
    def _make_user_input_device():
        return inputs.devices.gamepads[0]

    @staticmethod
    def _get_parser():
        return gamepad_events.GamepadInputEvent.from_raw_input_event
