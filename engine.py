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

    def get_status(self):
        return {
            "temperature": self.read_temperature(),
            "potentiometer": self.read_potentiometer(),
            "button1": self.read_button_state(),
            "led_on": self.led_on,
            "pins": [
                {"pin": 25, "label": "Button 1", "value": self.read_button_state()},
                {"pin": 12, "label": "Red LED", "value": self.led_on},
                {"pin": 39, "label": "Potentiometer", "value": self.read_potentiometer()},
            ]
        }

