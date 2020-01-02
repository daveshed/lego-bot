import threading
import inputs

from daveshed.legobot.inputs.base import UserInputEventBase


class MouseInputEvent(UserInputEventBase):

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
            raise AssertionError(
                "Unrecognised event (%r; %r)" % (event.code, event.state))

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
            raise AssertionError(
                "Unrecognised event (%r; %r)" % (event.code, event.state))


class MouseMovement(MouseInputEvent):

    def __init__(self, event):
        self._delta = event.state
        super().__init__(event)

    @property
    def delta(self):
        return self._delta


class MouseMovedX(MouseMovement): pass
class MouseMovedY(MouseMovement): pass
class WheelMoved(MouseMovement): pass
class LeftButtonClicked(MouseInputEvent): pass
class LeftButtonReleased(MouseInputEvent): pass
class RightButtonClicked(MouseInputEvent): pass
class RightButtonReleased(MouseInputEvent): pass
class MiddleButtonClicked(MouseInputEvent): pass
class MiddleButtonReleased(MouseInputEvent): pass
