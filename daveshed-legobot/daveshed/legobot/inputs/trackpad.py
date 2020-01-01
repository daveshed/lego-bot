import threading
import inputs

from daveshed.legobot.inputs import base as events


class TrackpadInputEvent(events.UserInputEventBase):

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
            ('BTN_RIGHT', 0,): RightButtonReleased,
            ('BTN_TOUCH', 1,): PadTouched,
            ('BTN_TOUCH', 0,): PadReleased,
        }
        try:
            event_type = event_map[(event.code, event.state,)]
            return event_type(event)
        except KeyError:
            return None


class TrackpadMovedX(events.AbsolutePositionX): pass
class TrackpadMovedY(events.AbsolutePositionY): pass
class LeftButtonClicked(events.ButtonClicked): pass
class LeftButtonReleased(events.ButtonReleased): pass
class RightButtonClicked(events.ButtonClicked): pass
class RightButtonReleased(events.ButtonReleased): pass
class PadTouched(events.ButtonClicked): pass
class PadReleased(events.ButtonReleased): pass
