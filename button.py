
from machine import Pin, Timer
import micropython
import time


class Button:
  DEBOUNCING_TIME = 10
  CHECK_RELEASED_TIME = 50

  def __init__(self, btn_pin_num, led_pin_num, ext_callback_pressed=None,
               ext_callback_released=None):
    self.btn_pin = Pin(btn_pin_num, Pin.IN, Pin.PULL_UP)
    self.led_pin = Pin(led_pin_num, Pin.OUT, value=0)

    self.pressed = False
    self.last_time_pressed = 0
    self.btn_pin.irq(self.btn_callback, Pin.IRQ_FALLING)
    self.check_released_timer = Timer(-1)

    self.ext_callback_pressed = ext_callback_pressed
    self.ext_callback_released = ext_callback_released

  @property
  def pressed_raw(self):
    return bool(1 - self.btn_pin.value())

  @property
  def led_value(self):
    return bool(self.led_pin.value())

  def led_set(self, state):
    self.led_pin.value(state)

  def led_toggle(self):
    self.led_set(not self.led_value)
  
  def led_off(self):
    self.led_set(0)
  
  def led_on(self):
    self.led_set(1)

  def btn_callback(self, _):
    # TODO: Look into schedule queue full error
    # TODO: Fix Neopixel glitches when pressing buttons
    # TODO: Determine if using timers or threads is a better option
    
    time_pressed = time.ticks_ms()
    if time_pressed - self.last_time_pressed > Button.DEBOUNCING_TIME:
      if self.pressed:
        self.btn_callback_released()
      else:
        self.btn_callback_pressed()
    self.last_time_pressed = time_pressed

  def btn_callback_pressed(self):
    self.check_released_timer.init(mode=Timer.ONE_SHOT,
                                   period=Button.CHECK_RELEASED_TIME,
                                   callback=self.check_released)
    self.pressed = True
    self.btn_pin.irq(self.btn_callback, Pin.IRQ_RISING)

    if self.ext_callback_pressed:
      micropython.schedule(self.ext_callback_pressed, self)

  def btn_callback_released(self):
    self.check_released_timer.deinit()
    self.pressed = False
    self.btn_pin.irq(self.btn_callback, Pin.IRQ_FALLING)

    if self.ext_callback_released:
      micropython.schedule(self.ext_callback_released, self)

  def check_released(self, _):
    if not self.pressed_raw:
      self.btn_callback_released()