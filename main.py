from button import Button
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

BUTTON_PIN_NUMS = ((12, 13), (14, 15), (16, 17), (19, 20))


def demo(buttons, leds):
    # Button LED flash
    for _ in range(10):
        for button in buttons:
            button.led_toggle()
        time.sleep(0.1)

    # Button LED chase
    for _ in range(5):
        for button in buttons:
            button.led_on()
            time.sleep(0.1)
            button.led_off()

    # Neopixels fill all
    for color in leds.COLORS.values():       
        leds.fill_all(color)
        leds.show_pixels()
        time.sleep(0.2)

    # Neopixels fill by group
    for _ in range(10):
        for led_group in leds.led_groups.values():
            led_group.fill(random.choice(list(leds.COLORS.values())))
        leds.show_pixels()
        time.sleep(0.2)

    # Neopixels chase by group
    for led_group in leds.led_groups.values():
        random_color = random.choice(list(leds.COLORS.values()))
        for color in [random_color, leds.COLORS['black']]:
            for i in range(led_group.num_leds):
                led_group.pixels[i].value = color
                leds.show_pixels()


if __name__ == '__main__':
    buttons = [Button(*pin_nums) for pin_nums in BUTTON_PIN_NUMS]
    leds = Leds(LED_GROUPS, BRIGHTNESS, PIN_NUM)

    demo(buttons, leds)
