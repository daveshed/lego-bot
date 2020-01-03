"""
Mouse device event definitions
"""
from daveshed.legobot.events import base as events


class MouseInputEvent(events.UserInputEventBase):
    """
    Mouse input event base class
    """
    @staticmethod
    def _parse_movement_event(event):
        event_map = {
            'REL_X': MouseMovedX,
            'REL_Y': MouseMovedY,
            'REL_WHEEL': WheelMoved,
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
            ('BTN_MIDDLE', 1,): MiddleButtonClicked,
            ('BTN_MIDDLE', 0,): MiddleButtonReleased,
        }
        try:
            event_type = event_map[(event.code, event.state,)]
            return event_type(event)
        except KeyError:
            return None

# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods,
# pylint: disable=multiple-statements
# pylint: disable=abstract-method
class MouseMovedX(events.RelativePositionX): pass
class MouseMovedY(events.RelativePositionY): pass
class WheelMoved(events.RelativePositionY): pass
class LeftButtonClicked(events.ButtonClicked): pass
class LeftButtonReleased(events.ButtonReleased): pass
class RightButtonClicked(events.ButtonClicked): pass
class RightButtonReleased(events.ButtonReleased): pass
class MiddleButtonClicked(events.ButtonClicked): pass
class MiddleButtonReleased(events.ButtonReleased): pass
