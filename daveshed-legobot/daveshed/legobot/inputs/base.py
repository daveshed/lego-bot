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

    def __init__(self, event):
        self._timestamp = event.timestamp

    @property
    def is_real_time(self):
        return time.time() - self.timestamp < self._DEADLINE_SEC

    @property
    def timestamp(self):
        return self._timestamp

    @classmethod
    def register_handler(cls, handler):
        cls._handlers[cls] = handler

    @classmethod
    def deregister_handler(cls):
        cls._handlers.pop(cls)

    def consume(self):
        try:
            callback = self._handlers[type(self)]
            callback(self)
        except KeyError:
            # no handler registered
            pass

    @classmethod
    def from_raw_input_event(cls, event):
        """
        Parse a raw input event from a user input device into a subclass.
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
            else:
                return None
        except KeyError:
            raise AssertionError("Unknown event %r" % event)

    @staticmethod
    def _parse_movement_event(event):
        raise NotImplementedError

    @staticmethod
    def _parse_key_event(event):
        raise NotImplementedError


class UserInputEventConsumer(threading.Thread):
    _DEADLINE_SEC = 0.2

    def __init__(self, device, event_type, *args, **kwargs):
        self.stop = threading.Event()
        self._device = device
        self._event_type = event_type
        super().__init__(*args, **kwargs)

    def run(self):
        while not self.stop.is_set():
            try:
                [raw_event] = self._device.read()
                _LOGGER.debug("Captured input event <%r, %r, %r>",
                    raw_event.ev_type, raw_event.code, raw_event.state)
            except inputs.UnknownEventCode as error:
                _LOGGER.warning("Unknown event error: %r" % error)
            parsed_event = self._event_type.from_raw_input_event(raw_event)
            if parsed_event:
                _LOGGER.debug("Got event %r", parsed_event)
                if parsed_event.is_real_time:
                    parsed_event.consume()
                else:
                    _LOGGER.warning("Event is not real time. Rejected.")
