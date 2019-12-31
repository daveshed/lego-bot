import threading
import inputs

from daveshed.legobot.inputs.base import UserInputEventBase


class GamepadInputEvent(UserInputEventBase):

    @staticmethod
    def _parse_movement_event(event):
        event_map = {
            ('ABS_Y', 255,): UpDpadPressed,
            ('ABS_Y', 127,): UpDpadReleased,
            ('ABS_Y', 0,): DownDpadPressed,
            ('ABS_Y', 127,): DownDpadReleased,
            ('ABS_X', 0,): LeftDpadPressed,
            ('ABS_X', 127,): LeftDpadReleased,
            ('ABS_X', 255,): RightDpadPressed,
            ('ABS_X', 127,): RightDpadReleased,
        }
        try:
            event_type = event_map[(event.code, event.state,)]
            return event_type(event)
        except KeyError:
            raise AssertionError(
                "Unrecognised event (%r; %r)" % (event.code, event.state))

    @staticmethod
    def _parse_key_event(event):
        event_map = {
            ('BTN_THUMB', 1,): AButtonPressed,
            ('BTN_THUMB', 0,): AButtonReleased,
            ('BTN_THUMB2', 1,): BButtonPressed,
            ('BTN_THUMB2', 0,): BButtonReleased,
            ('BTN_TRIGGER', 1,): XButtonPressed,
            ('BTN_TRIGGER', 0,): XButtonReleased,
            ('BTN_TOP', 0,): YButtonPressed,
            ('BTN_TOP', 1,): YButtonReleased,
            ('BTN_BASE4', 1,): StartButtonPressed,
            ('BTN_BASE4', 0,): StartButtonReleased,
            ('BTN_BASE3', 1,): SelectButtonPressed,
            ('BTN_BASE3', 1,): SelectButtonReleased,
            ('BTN_TOP2', 1,): LeftBumperPressed,
            ('BTN_TOP2', 0,): LeftBumperReleased,
            ('BTN_PINKIE', 1,): RightBumperPressed,
            ('BTN_PINKIE', 0,): RightBumperReleased,
        }
        try:
            event_type = event_map[(event.code, event.state,)]
            return event_type(event)
        except KeyError:
            raise AssertionError(
                "Unrecognised event (%r; %r)" % (event.code, event.state))


class AButtonPressed(GamepadInputEvent): pass
class AButtonReleased(GamepadInputEvent): pass
class BButtonPressed(GamepadInputEvent): pass
class BButtonReleased(GamepadInputEvent): pass
class XButtonPressed(GamepadInputEvent): pass
class XButtonReleased(GamepadInputEvent): pass
class YButtonPressed(GamepadInputEvent): pass
class YButtonReleased(GamepadInputEvent): pass
class StartButtonPressed(GamepadInputEvent): pass
class StartButtonReleased(GamepadInputEvent): pass
class SelectButtonPressed(GamepadInputEvent): pass
class SelectButtonReleased(GamepadInputEvent): pass
class LeftBumperPressed(GamepadInputEvent): pass
class LeftBumperReleased(GamepadInputEvent): pass
class RightBumperPressed(GamepadInputEvent): pass
class RightBumperReleased(GamepadInputEvent): pass
class UpDpadPressed(GamepadInputEvent): pass
class UpDpadReleased(GamepadInputEvent): pass
class DownDpadPressed(GamepadInputEvent): pass
class DownDpadReleased(GamepadInputEvent): pass
class LeftDpadPressed(GamepadInputEvent): pass
class LeftDpadReleased(GamepadInputEvent): pass
class RightDpadPressed(GamepadInputEvent): pass
class RightDpadReleased(GamepadInputEvent): pass
