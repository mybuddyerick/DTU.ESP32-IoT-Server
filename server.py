import machine
import network
import socket

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'ESP32-Group-1', authmode = 3, password = 'ra2ra2ra2')

pin_numbers = (13, 12, 27, 33, 15, 32, 14, 22, 23)
pins = [machine.Pin(i, machine.Pin.IN) for i in pin_numbers]

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

try:
    with open('index.html', 'r') as f:
        html = f.read()
except:
    FileNotFoundError('index.html not found')

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        #print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%d</td><td>%d</td></tr>' % (pin_numbers[i], pins[i].value()) for i in range(len(pins))]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
