import logging

from daveshed.legobot.application import Application
from daveshed.legobot.factory import TrackpadRobotStubFactory

logging.basicConfig(level=logging.INFO)

factory = TrackpadRobotStubFactory()
Application(factory).start()
