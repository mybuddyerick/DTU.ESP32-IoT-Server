from machine import Pin, ADC, PWM, I2C
import time
import mcp9808

class ESP32Controller:
    def __init__(self):
        self.button = Pin(25, Pin.IN, Pin.PULL_UP)

        # RGB LED Pins
        self.led_pins = {
            'red': PWM(Pin(12), freq=1000),
            'green': PWM(Pin(33), freq=1000),
            'blue': PWM(Pin(15), freq=1000)
        }

        # Initialize LED state
        self.led_on = False

        # Potentiometer
        self.pot = ADC(Pin(39))
        self.pot.atten(ADC.ATTN_11DB)

        # Temperature Sensor
        self.i2c = I2C(scl=Pin(22), sda=Pin(23))
        self.temp_sensor = mcp9808.MCP9808(self.i2c)

        # Button press state memory
        self.last_button_state = self.button.value()

    def read_temperature(self):
        return self.temp_sensor.read_temperature()

    def read_potentiometer(self):
        return self.pot.read()

    def read_button_state(self):
        return 0 if self.button.value() else 1  # Inverted logic

    def toggle_led(self):
        self.led_on = not self.led_on
        self.update_led()

    def update_led(self):
        brightness = self.read_potentiometer() // 4  # Scale 0–1023 to 0–255
        if self.led_on:
            self.led_pins['red'].duty(brightness)
            self.led_pins['green'].duty(0)
            self.led_pins['blue'].duty(0)
        else:
            for led in self.led_pins.values():
                led.duty(0)

    def check_button_toggle(self):
        current = self.button.value()
        if self.last_button_state == 1 and current == 0:
            self.toggle_led()
            time.sleep_ms(200)  # debounce
        self.last_button_state = current

    def get_rgb_brightness(self):
        return {
            "red": self.led_pins['red'].duty(),
            "green": self.led_pins['green'].duty(),
            "blue": self.led_pins['blue'].duty()
        }

    def get_status(self):
        rgb = self.get_rgb_brightness()
        return {
            "temperature": self.read_temperature(),
            "potentiometer": self.read_potentiometer(),
            "button1": self.read_button_state(),
            "rgb_brightness": rgb,
            "pins": [
                {"label": "Temperature Sensor - SCL", "pin": 22, "value": "I2C"},
                {"label": "Temperature Sensor - SDA", "pin": 23, "value": "I2C"},
                {"label": "Potentiometer", "pin": 39, "value": self.read_potentiometer()},
                {"label": "RGB LED - Red", "pin": 12, "value": rgb["red"]},
                {"label": "RGB LED - Green", "pin": 33, "value": rgb["green"]},
                {"label": "RGB LED - Blue", "pin": 15, "value": rgb["blue"]},
                {"label": "Button 1", "pin": 25, "value": self.read_button_state()}
            ]
        }
