import traceback
from threading import Event

from corobot.common import CorobotException

class Future():

    def __init__(self):
        self._data = None
        self._error = None
        self._event = Event()
        self._callbacks = []
        self._error_callbacks = []

    def wait(self):
        self._event.wait()
        if isinstance(self._error, str):
            raise CorobotException(self._error)
        elif isinstance(self._error, BaseException):
            raise self._error

    def then(self, callback=None, error=None):
        if callback is not None:
            if not callable(callback):
                raise TypeError("Callback must be callable.")
            self._callbacks.append(callback)
        if error is not None:
            if not callable(error):
                raise TypeError("Error callback must be callable.")
            self._error_callbacks.append(error)
        return self

    def get(self):
        self.wait()
        return self._data

    def is_fulfilled(self):
        return self._event.is_set()

    def _safe_call(self, f, data=None):
        try:
            if data is None:
                f()
            elif isinstance(data, tuple):
                f(*data)
            else:
                f(data)
        except:
            traceback.print_exc()

    def _fulfilled(self, data):
        self._data = data
        for callback in self._callbacks:
            self._safe_call(callback, data)
        self._event.set()

    def _error_occured(self, error):
        self._error = error
        for error_callback in self._error_callbacks:
            self._safe_call(error_callback, error)
        self._event.set()
