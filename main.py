from leds import Leds
import time

NUM_LEDS = 120
PIN_NUM = 18
BRIGHTNESS = 0.1


if __name__ == '__main__':
    leds = Leds(NUM_LEDS, BRIGHTNESS, PIN_NUM)
    for color in leds.COLORS.values():       
        leds.fill_pixels(color)
        leds.show_pixels()
        time.sleep(0.2)

    print('chases')
    for color in leds.COLORS.values():       
        for i in range(120):
            leds.led_array[i] = color
            leds.show_pixels()