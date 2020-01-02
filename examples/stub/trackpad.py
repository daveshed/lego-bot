import logging

import inputs

from daveshed.legobot.controller import TrackpadController
from daveshed.legobot.events import trackpad as trackpad_events
from daveshed.legobot.events.base import UserInputEventConsumer
from daveshed.legobot.robot import RobotStub

logging.basicConfig(level=logging.INFO)

# A human input device...
mouse = inputs.devices.mice[0]
# A stubbed robot implementation so we can demo without hardware...
robot = RobotStub()
# Now create and run the trackpad controller and wire it up to the robot...
controller = TrackpadController(robot)
controller.register_handlers(trackpad_events)
reader = UserInputEventConsumer(
    device=mouse,
    event_type=trackpad_events.TrackpadInputEvent,
    daemon=True)
reader.start()
