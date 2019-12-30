import threading
import inputs


class MouseInputEvent:
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
                "Relative": MouseMovement.from_input_event,
                "Sync": None,
                "Misc": None,
                "Key": ButtonClick.from_input_event,
            }[event.ev_type]
            if handler:
                return handler(event)
            else:
                return None
        except KeyError:
            raise AssertionError("Unknown event %r" % event)


class MouseMovement(MouseInputEvent):

    def __init__(self, delta, timestamp):
        self._delta = delta
        self._timestamp = timestamp

    @property
    def delta(self):
        return self._delta

    @staticmethod
    def from_input_event(event):
        if event.code == "REL_X":
            return MouseMovedX(event.state, event.timestamp)
        if event.code == "REL_Y":
            return MouseMovedY(event.state, event.timestamp)
        if event.code == "REL_WHEEL":
            return WheelMoved(event.state, event.timestamp)
        raise AssertionError("Unknown code %r" % event.code)

    def __repr__(self):
        return type(self).__name__ + ": " + str(self.delta)


class MouseMovedX(MouseMovement): pass


class MouseMovedY(MouseMovement): pass


class WheelMoved(MouseMovement): pass


class ButtonClick(MouseInputEvent):

    def __init__(self, timestamp):
        self._timestamp = timestamp

    @staticmethod
    def from_input_event(event):
        if event.code == "BTN_LEFT":
            if event.state == 1:
                return LeftButtonClicked(event.timestamp)
            if event.state == 0:
                return LeftButtonReleased(event.timestamp)
            raise AssertionError("Unknown state %r" % event.state)
        if event.code == "BTN_RIGHT":
            if event.state == 1:
                return RightButtonClicked(event.timestamp)
            if event.state == 0:
                return RightButtonReleased(event.timestamp)
            raise AssertionError("Unknown state %r" % event.state)
        if event.code == "BTN_MIDDLE":
            if event.state == 1:
                return RightButtonClicked(event.timestamp)
            if event.state == 0:
                return RightButtonReleased(event.timestamp)
            raise AssertionError("Unknown state %r" % event.state)
        raise AssertionError("Unknown code %r" % event.code)


class LeftButtonClicked(ButtonClick): pass


class LeftButtonReleased(ButtonClick): pass


class RightButtonClicked(ButtonClick): pass


class RightButtonReleased(ButtonClick): pass


class MiddleButtonClicked(ButtonClick): pass


class MiddleButtonReleased(ButtonClick): pass


class MouseReader(threading.Thread):

    def __init__(self, *args, **kwargs):
        self.stop = threading.Event()
        super().__init__(*args, **kwargs)

    def run(self):
        mouse = inputs.devices.mice[0]
        while not self.stop.is_set():
            try:
                [event] = mouse.read()
            except inputs.UnknownEventCode as error:
                print("WTF!... %r" % error)


            result = MouseInputEvent.from_input_event(event)
            if result:
                print(result)
                if result.handler:
                    result.handler()

