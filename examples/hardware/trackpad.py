import logging

from daveshed.legobot.application import Application
from daveshed.legobot.factory import TrackpadLegoRobotFactory

logging.basicConfig(level=logging.INFO)

factory = TrackpadLegoRobotFactory()
application = Application(factory)
application.start()
