import logging

from daveshed.legobot.application import Application
from daveshed.legobot.factory import MouseLegoRobotFactory

logging.basicConfig(level=logging.INFO)

factory = MouseLegoRobotFactory()
application = Application(factory)
application.start()
