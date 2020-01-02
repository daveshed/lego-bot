import logging

from daveshed.legobot.inputs import trackpad as controller
from daveshed.legobot.robot import RobotStub
from daveshed.legobot.controller import TrackpadController
from daveshed.legobot.inputs import trackpad

logging.basicConfig(level=logging.INFO)

robot = RobotStub()
controller = TrackpadController(robot)
controller.register_handlers(trackpad)

from daveshed.legobot.inputs.base import UserInputEventConsumer
from daveshed.legobot.inputs.trackpad import TrackpadInputEvent
import inputs

mouse = inputs.devices.mice[0]

reader = UserInputEventConsumer(
    device=mouse,
    event_type=TrackpadInputEvent,
    daemon=True)
reader.start()

