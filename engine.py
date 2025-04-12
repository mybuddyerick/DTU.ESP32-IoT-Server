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

def turn_off_led():
    red_pwm.duty(0)
    green_pwm.duty(0)
    blue_pwm.duty(0)

# -- button detection --

button1 = Pin(25, Pin.IN, Pin.PULL_UP)
button2 = Pin(34, Pin.IN, Pin.PULL_UP)

led_on = True
prev_button1_state = 1 # not pressed

def toggle_led():
    global led_on
    led_on = not led_on
    if not led_on:
        turn_off_led()

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

# -- loop --

def run_engine():
    global prev_button1_state
    while True:
        pot_val = pot.read()
        pwm = pwm = int((pot_val / 4095) * 1023)

        temp = sensor.temperature
        print(f"\rPotentiometer: {(pot_val/4095)*100:.1f}% | PWM: {pwm} | Temperature: {temp:.1f} °C", end='')

        current_state = button1.value()
        if prev_button1_state == 1 and current_state == 0:
            toggle_led()
        prev_button1_state = current_state
        button2_state = button2.value()

        if led_on:
            if temp < 23:
                set_green(pwm)
            elif temp < 24.5:
                set_blue(pwm)
            else:
                set_red(pwm)
        else:
            turn_off_led()
        time.sleep(0.1)

run_engine()
