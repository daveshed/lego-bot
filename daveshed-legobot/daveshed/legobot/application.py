"""
Application class definitions
"""
import abc

from daveshed.legobot.events.base import UserInputEventConsumer


class AbstractApplicationFactory(abc.ABC):
    """
    Abstract factory required by the application class to create dependencies
    """
    def __init__(self):
        self._robot = self._make_robot()

    # pylint: disable=too-few-public-methods
    def make_event_consumer(self):
        """
        Make an event consumer to take input events from the user input device
        and consume them.
        """
        self._register_controller()
        return UserInputEventConsumer(
            device=self._make_user_input_device(),
            parser=self._get_parser(),
            daemon=True)

    @property
    def robot(self):
        return self._robot

    @abc.abstractmethod
    def _register_controller(self):
        return

    @staticmethod
    @abc.abstractmethod
    def _make_user_input_device():
        return

    @staticmethod
    @abc.abstractmethod
    def _get_parser():
        return

    @abc.abstractmethod
    def _make_robot(self):
        return


class Application:
    """
    The robot controller application that can start and stop itself, creating
    and terminating dependencies as required.

    Args:
        factory (daveshed.legobot.application.AbstractApplicationFactory):
            a concrete instance of an application factory that creates
            dependencies.
    """
    def __init__(self, factory):
        self._robot = factory.robot
        self._event_consumer = factory.make_event_consumer()

    def start(self):
        """Start the application"""
        self._event_consumer.start()

    def terminate(self):
        """Graceful teardown the application"""
        self._robot.home()
        self._event_consumer.terminate()
