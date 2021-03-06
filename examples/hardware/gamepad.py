import logging

from daveshed.legobot.application import Application
from daveshed.legobot.factory import GamepadLegoRobotFactory

logging.basicConfig(level=logging.INFO)

factory = GamepadLegoRobotFactory()
application = Application(factory)
application.start()
