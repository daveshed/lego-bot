import threading
import inputs

from daveshed.legobot.inputs.base import UserInputEventBase


class TrackpadInputEvent(UserInputEventBase):

    @staticmethod
    def _parse_movement_event(event):
        event_map = {
            'ABS_X': TrackpadMovedX,
            'ABS_Y': TrackpadMovedY,
        }
        try:
            event_type = event_map[event.code]
            return event_type(event)
        except KeyError:
            return None

    @staticmethod
    def _parse_key_event(event):
        event_map = {
            ('BTN_LEFT', 1,): LeftButtonClicked,
            ('BTN_LEFT', 0,): LeftButtonReleased,
            ('BTN_RIGHT', 1,): RightButtonClicked,
            ('BTN_RIGHT', 0,): RightButtonReleased,            ('BTN_MIDDLE', 1,): MiddleButtonClicked,
        }
        try:
            event_type = event_map[(event.code, event.state,)]
            return event_type(event)
        except KeyError:
            return None


class TrackpadMovement(TrackpadInputEvent):

    def __init__(self, event):
        self._position = event.state
        super().__init__(event)

    @property
    def position(self):
        return self._position


class TrackpadMovedX(TrackpadMovement): pass
class TrackpadMovedY(TrackpadMovement): pass
class WheelMoved(TrackpadMovement): pass
class LeftButtonClicked(TrackpadInputEvent): pass
class LeftButtonReleased(TrackpadInputEvent): pass
class RightButtonClicked(TrackpadInputEvent): pass
class RightButtonReleased(TrackpadInputEvent): pass
class MiddleButtonClicked(TrackpadInputEvent): pass
class MiddleButtonReleased(TrackpadInputEvent): pass
