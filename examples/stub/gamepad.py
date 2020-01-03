import logging

import inputs

from daveshed.legobot.controller import GamepadController
from daveshed.legobot.events import gamepad as gamepad_events
from daveshed.legobot.events.base import UserInputEventConsumer
from daveshed.legobot.robot import RobotStub

logging.basicConfig(level=logging.INFO)

# A human input device...
gamepad = inputs.devices.gamepads[0]
# A stubbed robot implementation so we can demo without hardware...
robot = RobotStub()
# Now create and run the gamepad controller and wire it up to the robot...
controller = GamepadController(robot)
controller.register_handlers(gamepad_events)
reader = UserInputEventConsumer(
    device=gamepad,
    parser=gamepad_events.GamepadInputEvent.from_raw_input_event,
    daemon=True)
reader.start()
