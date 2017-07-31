from common.colors import Color, color_name
from proto import BUTTON_NAMES
import random
import time


class Interface:
    def __init__(self):
        self.badges = {}

    def register_badge(self, badge):
        self.badges[int(badge.mac)] = badge

    def run(self):
        while True:
            if not self.badges:
                time.sleep(1)
                continue
            badge = random.choice(list(self.badges.values()))
            button = random.choice(list(BUTTON_NAMES.values()))
            badge.on_button_press(button)
            time.sleep(.05)
            badge.on_button_release(button)
            time.sleep(1)

    def show_lights(self, badge_id, *color_args):
        color_names = [color_name(Color(c).rgb) for c in color_args]
        print("{!s}: LIGHTS [{:^11s}] [{:^11s}] [{:^11s}] [{:^11s}]".format(badge_id, *color_names))
