import logging

import inputs

from daveshed.legobot.controller import MouseController
from daveshed.legobot.events import mouse as mouse_events
from daveshed.legobot.events.base import UserInputEventConsumer
from daveshed.legobot.robot import RobotStub

logging.basicConfig(level=logging.INFO)

# A human input device...
mouse = inputs.devices.mice[0]
# A stubbed robot implementation so we can demo without hardware...
robot = RobotStub()
# Now create and run the mouse controller...
controller = MouseController(robot)
#... and wire it up to the robot...
controller.register_handlers(mouse_events)
# Create and run a worker to service the raw inputs from the mouse...
reader = UserInputEventConsumer(
    device=mouse,
    parser=mouse_events.MouseInputEvent.from_raw_input_event,
    daemon=True)
reader.start()
