import abc
import logging
import threading

_LOGGER = logging.getLogger("GRASPER")


class Grasper(abc.ABC):

    @abc.abstractmethod
    def open(self):
        """Open the grasper"""

    @abc.abstractmethod
    def close(self):
        """Close the grasper"""

    @property
    @abc.abstractmethod
    def is_open(self):
        """
        The current status of the grasper

        Returns;
            bool: True if the grasper is open
        """


class LegoServoGrasper(Grasper):
    _OPEN_ANGLE = 65.0
    _CLOSED_ANGLE = 90.0

    def __init__(self, servo):
        self._servo = servo
        self._is_open = None
        self._lock = threading.Lock()
        self.open()

    def open(self):
        _LOGGER.info("OPENING...")
        with self._lock:
            self._servo.angle = self._OPEN_ANGLE
            self._is_open = True

    def close(self):
        _LOGGER.info("CLOSING...")
        with self._lock:
            self._servo.angle = self._CLOSED_ANGLE
            self._is_open = False

    @property
    def is_open(self):
        return self._is_open

