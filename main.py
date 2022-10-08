from collections import OrderedDict
from leds import Leds
import random
import time

PIN_NUM = 18
BRIGHTNESS = 0.1
LED_GROUPS = OrderedDict([('ring0', 12),
                          ('ring1', 12),
                          ('ring2', 12),
                          ('ring3', 12),
                          ('strip', 72)])


if __name__ == '__main__':
    leds = Leds(LED_GROUPS, BRIGHTNESS, PIN_NUM)

    # Fill all
    for color in leds.COLORS.values():       
        leds.fill_all(color)
        leds.show_pixels()
        time.sleep(0.2)

    # Fill by group
    for _ in range(10):
        for group in leds.led_values.keys():
            leds.fill_group(group, random.choice(list(leds.COLORS.values())))
        leds.show_pixels()
        time.sleep(0.4)

    # Chase by group
    for group in leds.led_values.keys():
        random_color = random.choice(list(leds.COLORS.values()))
        for color in [random_color, leds.COLORS['black']]:
            for i in range(len(leds.led_values[group])):
                leds.led_values[group][i] = color
                leds.show_pixels()