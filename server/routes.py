import os
import time
import threading
from flask import Blueprint, request, jsonify
from lights import controller
from constants import DEFAULT_DIMMING, DEFAULT_DURATION, COLORS

events_bp = Blueprint("events", __name__)


def _authorized() -> bool:
    api_key = os.getenv("BLACKVINE_API_KEY", "")
    if not api_key:
        return True
    return request.headers.get("X-Api-Key", "") == api_key


def _configured_bulbs() -> dict[str, str]:
    return {
        k[5:].lower(): v
        for k, v in os.environ.items()
        if k.startswith("BULB_")
    }


@events_bp.route("/event", methods=["POST"])
def receive_event():
    if not _authorized():
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}

    bulb_name = data.get("bulb", "").strip()
    if not bulb_name:
        return jsonify({"error": "'bulb' is required"}), 400

    ip = os.getenv(f"BULB_{bulb_name.upper()}")
    if not ip:
        return jsonify({"error": f"bulb '{bulb_name}' not configured (set BULB_{bulb_name.upper()})"}), 400

    color_name = data.get("color", "").lower()
    if color_name:
        if color_name not in COLORS:
            return jsonify({"error": f"unknown color '{color_name}'", "options": list(COLORS)}), 400
        r, g, b = COLORS[color_name]
    else:
        r = int(data.get("r", 255))
        g = int(data.get("g", 255))
        b = int(data.get("b", 255))

    dimming  = int(data.get("dimming",  DEFAULT_DIMMING))
    duration = int(data.get("duration", DEFAULT_DURATION))

    controller.set_bulb(ip, r, g, b, dimming, duration)
    return jsonify({"ok": True})


@events_bp.route("/test")
def test_lights():
    if not _authorized():
        return jsonify({"error": "unauthorized"}), 401

    bulbs = _configured_bulbs()
    if not bulbs:
        return jsonify({"error": "no bulbs configured"}), 400

    color_cycle = list(COLORS.keys())

    def _run():
        for i, (name, ip) in enumerate(bulbs.items()):
            r, g, b = COLORS[color_cycle[i % len(color_cycle)]]
            controller.set_bulb(ip, r, g, b, dimming=80, duration=3)
            time.sleep(3.5)

    threading.Thread(target=_run, daemon=True).start()
    return jsonify({"testing": list(bulbs.keys())})


@events_bp.route("/health")
def health():
    return jsonify({"status": "ok"})
