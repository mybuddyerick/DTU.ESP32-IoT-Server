from machine import Pin, I2C, PWM, ADC
import time
from mcp9808 import MCP9808

# -- I2C & Temp Sensor Setup --

i2c = I2C(scl=Pin(22), sda=Pin(23))
sensor = MCP9808(i2c)

# -- Potentiometer --

pot = ADC(Pin(39))
pot.atten(ADC.ATTN_11DB)
pot.width(ADC.WIDTH_12BIT)

# -- RGB setup --

red_pwm = PWM(Pin(12), freq=10000)
green_pwm = PWM(Pin(33), freq=10000)
blue_pwm = PWM(Pin(15), freq=10000)

# -- RGB color functions --

def set_green(pwm):
    red_pwm.duty(pwm)
    green_pwm.duty(0)
    blue_pwm.duty(pwm)

def set_blue(pwm):
    red_pwm.duty(pwm)
    green_pwm.duty(pwm)
    blue_pwm.duty(0)

def set_red(pwm):
    red_pwm.duty(0)
    green_pwm.duty(pwm)
    blue_pwm.duty(pwm)

# -- loop --

def run_engine():
    while True:
        # Read potentiometer and map to 0–1023 for brightness
        val = pot.read()
        val = val/4095
        pwm = int(1023 * val)

        temp = sensor.temperature
        print(f"\rPotentiometer: {val:.3f} | PWM: {pwm} | Temperature: {temp:.2f} °C", end='')

        if temp < 23:
            set_green(pwm)
        elif temp < 24.5:
            set_blue(pwm)
        else:
            set_red(pwm)        
        time.sleep(0.2)

run_engine()

def update_led_color():
    pot_val = pot.read()
    brightness = int((pot_val / 4095) * 1023)
    temp = sensor.temperature
    if temp < 26:
        set_green(brightness)
    elif temp < 27.5:
        set_blue(brightness)
    else:
        set_red(brightness)
