
from machine import Pin


class Button:
  def __init__(self, btn_pin_num, led_pin_num):
    self.btn_pin = Pin(btn_pin_num, Pin.IN, Pin.PULL_UP)
    self.led_pin = Pin(led_pin_num, Pin.OUT)

    self.led_off()

  @property
  def pressed(self):
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
