import logging

import inputs

from daveshed.legobot.controller import TrackpadController
from daveshed.legobot.events import trackpad as trackpad_events
from daveshed.legobot.events.base import UserInputEventConsumer
from daveshed.legobot.robot import RobotStub

logging.basicConfig(level=logging.INFO)

robot = RobotStub()
controller = TrackpadController(robot)
controller.register_handlers(trackpad_events)
mouse = inputs.devices.mice[0]
reader = UserInputEventConsumer(
    device=mouse,
    event_type=trackpad_events.TrackpadInputEvent,
    daemon=True)
reader.start()
