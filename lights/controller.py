import threading
from . import wiz
from constants import DEFAULT_DIMMING, DEFAULT_DURATION

_timers: dict[str, threading.Timer] = {}
_lock = threading.Lock()


def _cancel(key: str) -> None:
    t = _timers.pop(key, None)
    if t:
        t.cancel()


def _schedule(key: str, delay: float, fn, *args) -> None:
    with _lock:
        _cancel(key)
        t = threading.Timer(delay, fn, args)
        t.daemon = True
        t.start()
        _timers[key] = t


def set_bulb(ip: str, r: int, g: int, b: int,
             dimming: int = DEFAULT_DIMMING,
             duration: int = DEFAULT_DURATION) -> None:
    wiz.on(ip, r, g, b, dimming)
    if duration > 0:
        _schedule(ip, duration, wiz.off, ip)
