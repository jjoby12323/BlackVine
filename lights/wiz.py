import json
import socket
from constants import WIZ_PORT


def _send(ip: str, params: dict) -> None:
    msg = json.dumps({"method": "setPilot", "params": params}).encode()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(msg, (ip, WIZ_PORT))


def on(ip: str, r: int, g: int, b: int, dimming: int = 100) -> None:
    _send(ip, {"state": True, "r": r, "g": g, "b": b, "dimming": dimming})


def off(ip: str) -> None:
    _send(ip, {"state": False})
