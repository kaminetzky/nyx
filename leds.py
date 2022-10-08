import array, time
from machine import Pin
import rp2


class Leds:
    COLORS = {'black': (0, 0, 0),
              'white': (255, 255, 255),
              'red': (255, 0, 0),
              'green': (0, 255, 0),
              'blue': (0, 0, 255),
              'cyan': (0, 255, 255),
              'magenta': (180, 0, 255),
              'yellow': (255, 150, 0),
             }

    def __init__(self, num_leds, brightness, pin_num):
        self.num_leds = num_leds
        self.brightness = brightness

        self.led_array = [[0, 0, 0] for _ in range(num_leds)]
        self.state_machine = rp2.StateMachine(
            0, Leds.pio_program, freq=8_000_000, sideset_base=Pin(pin_num))
        self.state_machine.active(1)

    @staticmethod
    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
        autopull=True, pull_thresh=24)
    def pio_program():
        T1 = 2
        T2 = 5
        T3 = 3
        wrap_target()
        label('bitloop')
        out(x, 1)               .side(0)    [T3 - 1]
        jmp(not_x, 'do_zero')   .side(1)    [T1 - 1]
        jmp('bitloop')          .side(1)    [T2 - 1]
        label('do_zero')
        nop()                   .side(0)    [T2 - 1]
        wrap()

    def show_pixels(self):
        led_array_dimmed = array.array('I', [0 for _ in range(self.num_leds)])
        for i, rgb_value in enumerate(self.led_array):
            red_val, green_val, blue_val = rgb_value
            red_val_dimmed = int(red_val * self.brightness)
            green_val_dimmed = int(green_val * self.brightness)
            blue_val_dimmed = int(blue_val * self.brightness)
            led_array_dimmed[i] = ((green_val_dimmed<<16)
                                   + (red_val_dimmed<<8)
                                   + blue_val_dimmed)
        self.state_machine.put(led_array_dimmed, 8)

    def fill_pixels(self, color):
        self.led_array = [color for _ in range(self.num_leds)]
