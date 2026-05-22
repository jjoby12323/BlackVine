WIZ_PORT        = 38899  # fixed by WiZ UDP protocol
DEFAULT_DIMMING  = 100
DEFAULT_DURATION = 0     # 0 = stay on until the next event clears it

COLORS: dict[str, tuple[int, int, int]] = {
    "white":  (255, 255, 255),
    "red":    (255, 0,   0),
    "green":  (0,   255, 0),
    "blue":   (0,   0,   255),
    "cyan":   (0,   200, 255),
    "amber":  (255, 140, 0),
    "yellow": (255, 200, 0),
    "purple": (180, 0,   255),
}
