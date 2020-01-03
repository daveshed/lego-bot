"""
User interface input event definitions and base classes
"""
import logging
import threading
import time

import inputs

_LOGGER = logging.getLogger("INPUT")


class UserInputEventBase:
    """
    Baseclass for all user input events. These events may be consumed by the
    UserInputEventConsumer who will call the associated handler.
    """
    _handlers = {}
    _DEADLINE_SEC = 0.2
    _lock = threading.Lock()

    def __init__(self, event):
        self._timestamp = event.timestamp

    @property
    def is_real_time(self):
        """
        Indicates whether this event is stale

        Returns:
            bool: True if this event is younger than the configured deadline.
        """
        return time.time() - self.timestamp < self._DEADLINE_SEC

    @property
    def timestamp(self):
        """
        The timestamp associated with this event's creation

        Returns
            float: the timestamp
        """
        return self._timestamp

    @classmethod
    def register_handler(cls, handler):
        """
        Register a callback to be called when this event this event is consumed.
        Note that only one callback can be registered. Registering another will
        overwrite.

        Args:
            callable: the callback
        """
        with cls._lock:
            cls._handlers[cls] = handler

    @classmethod
    def deregister_handler(cls):
        """
        Deregister any callbacka that has previously been registered.
        """
        with cls._lock:
            try:
                cls._handlers.pop(cls)
            except KeyError:
                # no handler is registered so do nothing.
                pass

    def consume(self):
        """
        Consume this event instance by passing it to any registered callback
        """
        try:
            callback = self._handlers[type(self)]
            _LOGGER.debug("Calling handler %r", callback)
            callback(self)
        except KeyError:
            _LOGGER.debug("%r has no handlers", self)

    @classmethod
    def from_raw_input_event(cls, event):
        """
        A factory that parses a raw input events from a user input device into
        a recognisable event subclasses.

        Args:
            event: inputs.InputEvent

        Returns:
            UserInputEventBase: the specific event instance corresponding to the
                raw input event.
        """
        try:
            raw_event_handler = {
                "Relative": cls._parse_movement_event,
                "Absolute": cls._parse_movement_event,
                "Sync": None,
                "Misc": None,
                "Key": cls._parse_key_event,
            }[event.ev_type]
            if raw_event_handler:
                return raw_event_handler(event)
            return None
        except KeyError:
            raise AssertionError("Unknown event type %r" % event)

    @staticmethod
    def _parse_movement_event(event):
        raise NotImplementedError

    @staticmethod
    def _parse_key_event(event):
        raise NotImplementedError


class AbsolutePositionX(UserInputEventBase):
    """
    An absolute position update in the x-axis

    Args:
        event (inputs.InputEvent): the associated raw input event
    """
    # pylint: disable=abstract-method
    def __init__(self, event):
        self._position = event.state
        super().__init__(event)

    @property
    def position(self):
        """
        The position contained in this event

        Returns:
            float: the position
        """
        return self._position


class AbsolutePositionY(UserInputEventBase):
    """
    An absolute position update in the y-axis

    Args:
        event (inputs.InputEvent): the associated raw input event
    """
    # pylint: disable=abstract-method
    def __init__(self, event):
        self._position = event.state
        super().__init__(event)

    @property
    def position(self):
        """
        The position contained in this event

        Returns:
            float: the position
        """
        return self._position


class RelativePositionX(UserInputEventBase):
    """
    A relative position update in the x-axis

    Args:
        event (inputs.InputEvent): the associated raw input event
    """
    # pylint: disable=abstract-method
    def __init__(self, event):
        self._delta = event.state
        super().__init__(event)

    @property
    def delta(self):
        """
        Position change

        Returns:
            float: the position change
        """
        return self._delta


class RelativePositionY(UserInputEventBase):
    """
    A relative position update in the x-axis

    Args:
        event (inputs.InputEvent): the associated raw input event
    """
    # pylint: disable=abstract-method
    def __init__(self, event):
        self._delta = event.state
        super().__init__(event)

    @property
    def delta(self):
        """
        Position change

        Returns:
            float: the position change
        """
        return self._delta


# pylint: disable=abstract-method
class ButtonClicked(UserInputEventBase):
    """Button click event"""
# pylint: enable=abstract-method


# pylint: disable=abstract-method
class ButtonReleased(UserInputEventBase):
    """Button release event"""
# pylint: enable=abstract-method


class UserInputEventConsumer(threading.Thread):
    """
    A thread that consumes input device events

    Args:
        device (obj): a user input device
        event_parser (callable): parses raw input events
    """
    _DEADLINE_SEC = 0.2

    def __init__(self, device, parser, *args, **kwargs):
        self.stop = threading.Event()
        self._device = device
        self._parser = parser
        super().__init__(*args, **kwargs)

    def run(self):
        while not self.stop.is_set():
            event = self._get_next_event()
            if not event:
                continue
            if not event.is_real_time:
                self._handle_stale_event(event)
                continue
            self._handle_real_time_event(event)

    def _get_next_event(self):
        result = None
        try:
            [raw_event] = self._device.read()
            _LOGGER.debug(
                "Captured input event <%r, %r, %r>",
                raw_event.ev_type, raw_event.code, raw_event.state)
            result = self._parser(raw_event)
        except inputs.UnknownEventCode as error:
            _LOGGER.warning("Unknown event error: %r", error)
        return result

    @staticmethod
    def _handle_stale_event(event):
        _LOGGER.warning("Event %r is not real time. Rejected.", event)

    @staticmethod
    def _handle_real_time_event(event):
        _LOGGER.debug("Got event %r", event)
        event.consume()
