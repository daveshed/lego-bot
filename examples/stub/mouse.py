import logging

from daveshed.legobot.application import Application
from daveshed.legobot.factory import MouseRobotStubFactory

logging.basicConfig(level=logging.INFO)

factory = MouseRobotStubFactory()
Application(factory).start()
