import logging

from daveshed.legobot.application import Application
from daveshed.legobot.factory import GamepadRobotStubFactory

logging.basicConfig(level=logging.INFO)

factory = GamepadRobotStubFactory()
application = Application(factory).start()
