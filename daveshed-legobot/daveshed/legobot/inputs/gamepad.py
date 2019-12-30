import threading
import inputs


A_BUTTON_PRESSED = ('BTN_THUMB', 1,)
A_BUTTON_RELEASED = ('BTN_THUMB', 0,)
B_BUTTON_BUTTON = ('BTN_THUMB2', 1,)
B_BUTTON_RELEASED = ('BTN_THUMB2', 0,)
X_BUTTON_PRESSED = ('BTN_TRIGGER', 1,)
X_BUTTON_RELEASED = ('BTN_TRIGGER', 0,)
Y_BUTTON_PRESSED = ('BTN_TOP', 0,)
Y_BUTTON_RELEASED = ('BTN_TOP', 1,)
START_BUTTON_PRESSED = ('BTN_BASE4', 1,)
START_BUTTON_RELEASED = ('BTN_BASE4', 0,)
SELECT_BUTTON_PRESSED = ('BTN_BASE3', 1,)
SELECT_BUTTON_RELEASED = ('BTN_BASE3', 1,)
LEFT_BUMPER_PRESSED = ('BTN_TOP2', 1,)
LEFT_BUMPER_RELEASED = ('BTN_TOP2', 0,)
RIGHT_BUMPER_PRESSED = ('BTN_PINKIE', 1,)
RIGHT_BUMPER_RELEASED = ('BTN_PINKIE', 0,)
UP_DPAD_PRESSED = ('ABS_Y', 255,)
UP_DPAD_RELEASED = ('ABS_Y', 127,)
DOWN_DPAD_PRESSED = ('ABS_Y', 0,)
DOWN_DPAD_RELEASED = UP_DPAD_RELEASED
LEFT_DPAD_PRESSED = ('ABS_X', 0,)
LEFT_DPAD_RELEASED = ('ABS_X', 127,)
RIGHT_DPAD_PRESSED = ('ABS_X', 255,)
RIGHT_DPAD_RELEASED = LEFT_DPAD_RELEASED


class GamepadInputEvent:
    callback = None

    def handler(self):
        if self.callback:
            self.callback(self)

    @property
    def timestamp(self):
        return self._timestamp

    @staticmethod
    def from_input_event(event):
        try:
            handler = {
                "Absolute": DPadMovementEvent.from_input_event,
                "Sync": None,
                "Misc": None,
                "Key": PadButtonEvent.from_input_event,
            }[event.ev_type]
            if handler:
                return handler(event)
            else:
                return None
        except KeyError:
            raise AssertionError("Unknown event %r" % event)


class PadButtonEvent(GamepadInputEvent):

    def __init__(self, timestamp):
        self._timestamp = timestamp

    @staticmethod
    def from_input_event(event):
        try:
            event_type = {
                A_BUTTON_PRESSED: AButtonPressed,
                A_BUTTON_RELEASED: AButtonReleased,
                B_BUTTON_BUTTON: BButtonPressed,
                B_BUTTON_RELEASED: BButtonReleased,
                X_BUTTON_PRESSED: XButtonPressed,
                X_BUTTON_RELEASED: XButtonPressed,
                Y_BUTTON_PRESSED: YButtonPressed,
                Y_BUTTON_RELEASED: YButtonReleased,
                START_BUTTON_PRESSED: StartButtonPressed,
                START_BUTTON_RELEASED: StartButtonReleased,
                SELECT_BUTTON_PRESSED: SelectButtonPressed,
                SELECT_BUTTON_RELEASED: SelectButtonReleased,
                LEFT_BUMPER_PRESSED: LeftBumperPressed,
                LEFT_BUMPER_RELEASED: LeftBumperReleased,
                RIGHT_BUMPER_PRESSED: RightBumperPressed,
                RIGHT_BUMPER_RELEASED: RightBumperReleased,
            }[(event.code, event.state,)]
            return event_type(event.timestamp)
        except KeyError:
            raise AssertionError(
                "Unrecognised button event (%r; %r)"
                % (event.code, event.state))


class DPadMovementEvent(GamepadInputEvent):

    def __init__(self, timestamp):
        self._timestamp = timestamp

    @staticmethod
    def from_input_event(event):
        try:
            event_type = {
                UP_DPAD_PRESSED: UpDpadPressed,
                UP_DPAD_RELEASED: UpDpadReleased,
                DOWN_DPAD_PRESSED: DownDpadPressed,
                DOWN_DPAD_RELEASED: DownDpadReleased,
                LEFT_DPAD_PRESSED: LeftDpadPressed,
                LEFT_DPAD_RELEASED: LeftDpadReleased,
                RIGHT_DPAD_PRESSED: RightDpadPressed,
                RIGHT_DPAD_RELEASED: RightDpadReleased,
            }[(event.code, event.state,)]
            return event_type(event.timestamp)
        except KeyError:
            raise AssertionError(
                "Unrecognised button event (%r; %r)"
                % (event.code, event.state))


class AButtonPressed(PadButtonEvent): pass
class AButtonReleased(PadButtonEvent): pass
class BButtonPressed(PadButtonEvent): pass
class BButtonReleased(PadButtonEvent): pass
class XButtonPressed(PadButtonEvent): pass
class XButtonReleased(PadButtonEvent): pass
class YButtonPressed(PadButtonEvent): pass
class YButtonReleased(PadButtonEvent): pass
class StartButtonPressed(PadButtonEvent): pass
class StartButtonReleased(PadButtonEvent): pass
class SelectButtonPressed(PadButtonEvent): pass
class SelectButtonReleased(PadButtonEvent): pass
class LeftBumperPressed(PadButtonEvent): pass
class LeftBumperReleased(PadButtonEvent): pass
class RightBumperPressed(PadButtonEvent): pass
class RightBumperReleased(PadButtonEvent): pass
class UpDpadPressed(DPadMovementEvent): pass
class UpDpadReleased(DPadMovementEvent): pass
class DownDpadPressed(DPadMovementEvent): pass
class DownDpadReleased(DPadMovementEvent): pass
class LeftDpadPressed(DPadMovementEvent): pass
class LeftDpadReleased(DPadMovementEvent): pass
class RightDpadPressed(DPadMovementEvent): pass
class RightDpadReleased(DPadMovementEvent): pass


class GamepadReader(threading.Thread):

    def __init__(self, *args, **kwargs):
        self.stop = threading.Event()
        super().__init__(*args, **kwargs)

    def run(self):
        pad = inputs.devices.gamepads[0]
        while not self.stop.is_set():
            try:
                [event] = pad.read()
            except inputs.UnknownEventCode as error:
                print("WTF!... %r" % error)


            result = GamepadInputEvent.from_input_event(event)
            if result:
                print(result)
                if result.handler:
                    result.handler()
