from . import udp
from . import wamp

BUTTON_RIGHT = 1
BUTTON_DOWN = 2
BUTTON_LEFT = 3
BUTTON_UP = 4
BUTTON_SELECT = 5
BUTTON_START = 6
BUTTON_B = 7
BUTTON_A = 8

BUTTON_NAMES = {
    BUTTON_RIGHT: "right",
    BUTTON_DOWN: "down",
    BUTTON_LEFT: "left",
    BUTTON_UP: "up",
    BUTTON_SELECT: "select",
    BUTTON_START: "start",
    BUTTON_B: "b",
    BUTTON_A: "a",
}

BUTTON_IDS = {
    "right": BUTTON_RIGHT,
    "down": BUTTON_DOWN,
    "left": BUTTON_LEFT,
    "up": BUTTON_UP,
    "select": BUTTON_SELECT,
    "start": BUTTON_START,
    "b": BUTTON_B,
    "a": BUTTON_A
}


def button_bit(button_id):
    return 1 << (button_id - 1)
