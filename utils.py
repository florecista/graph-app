
import functools

from PyQt5.QtCore import QTimer


def populate_listwidget_enum(lw, enum):
    """Populates the given QListWidget from a Python Enum

    :param lw: QListWidget to populate.
    :type lw: QListWidget
    :param enum: Enum to load values from.
    :type enum: Enum
    """
    for v in enum:
        lw.addItem(v.name, v.value)


class signal_throttle:
    """This decorator can be applied to any receiving slot to throttle
    the incoming signals. It does this by silently dropping
    _all but the latest_ signal.

    When a signal is received, a timer is started. When the timer expires
    the data is sent to the slot. If other signals are received in the
    intervening time, they will replace the data.

    The timer will be unaffected i.e. continuous signals will not block
    _something_ from happening.
    """

    def __init__(self, msecs=100):
        self.timer = QTimer()
        self.timer.setInterval(msecs)
        self.timer.setSingleShot(True)

    def __call__(self, fn):
        # These hold the data to forward to the signal receiver.
        self.args = []
        self.kwargs = {}
        self._self = None

        def handler():
            # Call the slot.
            fn(self._self, *self.args, **self.kwargs)

        # After timer, the handler is called.
        self.timer.timeout.connect(handler)

        @functools.wraps(fn)
        def wrapper(_self, *args, **kwargs):
            self._self = _self
            self.args = args
            self.kwargs = kwargs

            if self.timer.isActive():
                return

            self.timer.start()

        return wrapper
