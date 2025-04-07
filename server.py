from machine import Pin, I2C, PWM, ADC
import network
import socket
from engine import sensor, pot, set_red, set_green, set_yellow, update_led_color

# -- setup network id --
ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'ESP32-Group-1', authmode = 3, password = 'ra2ra2ra2')

# -- Pin list for table --
pin_numbers = (13, 12, 27, 33, 15, 32, 14, 22, 23)
pins = [Pin(i, Pin.IN) for i in pin_numbers]

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

try:
    with open('index.html', 'r') as f:
        html = f.read()
except:
    print("index.html not found")

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        # print(line)
        if not line or line == b'\r\n':
            break
    
    update_led_color()

    # Pin Table
    rows = ['<tr><td>%d</td><td>%d</td></tr>' % (pin_numbers[i], pins[i].value()) for i in range(len(pins))]

    # Sensor Readings
    temp = sensor.temperature
    pot_val = pot.read()
    print(f"Temperature: {temp:.2f} °C | Potentiometer: {pot_val}")

    response = html % '\n'.join(rows)
    response = response.replace('</body>',f'<p>Temperature: {temp:.2f} °C</p><p>Potentiometer: {pot_val}</p></body>')

    cl.send(response)
    cl.close()
