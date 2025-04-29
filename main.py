'''
+------------------+------------+
|     Component    |   Pin(s)   |
+------------------+------------+
| Temp Sensor      | SCL - 22   |
|                  | SDA - 23   |
+------------------+------------+
| Potentiometer    | 39         |
+------------------+------------+
| RGB LED          | Red   - 12 |
|                  | Green - 33 |
|                  | Blue  - 15 |
+------------------+------------+
| Button 1         | 25         |
+------------------+------------+

'''

# main.py
import network
import socket
import ujson
from engine import ESP32Controller

controller = ESP32Controller()

# init WiFi Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='mini-Markus', authmode=3, password='ra2ra2ra2')

with open('index.html', 'r') as f:
    html_template = f.read()

# init Setup socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)

print("Server running on 192.168.4.1:80")

while True:
    controller.check_button_toggle()
    
    cl, addr = server.accept()
    print('Client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    request_line = cl_file.readline()
    print("Request:", request_line)

    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    # Parse route
    try:
        request_path = request_line.decode().split(' ')[1]
    except:
        request_path = '/'

    if request_path == '/api/data':
        data = controller.get_status()
        response = ujson.dumps(data)
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)

    elif request_path == '/api/pins':
        response = ujson.dumps(controller.get_status()["pins"])
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)

    elif request_path == '/api/temperature':
        response = ujson.dumps({"temperature": controller.read_temperature()})
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)

    elif request_path == '/api/potentiometer':
        response = ujson.dumps({"potentiometer": controller.read_potentiometer()})
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)

    elif request_path == '/api/button1':
        response = ujson.dumps({"button1": controller.read_button_state()})
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)

    elif request_path == '/api/rgb':
        response = ujson.dumps(controller.get_rgb_brightness())
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)

    elif request_path == '/toggle':
        controller.toggle_led()
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nLED toggled")

    elif '.' in request_path:
        try:
            with open(request_path, 'r') as f:
                cl.send(f.read())
        except:
            cl.send("HTTP/1.1 404 NO FILE\r\n\r\n")
    else:
        html = html_template
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.sendall(html)

    cl.close()
