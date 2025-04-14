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

# Set up WiFi Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='mini-Markus', authmode=3, password='ra2ra2ra2')

# Serve HTML
with open('index.html', 'r') as f:
    html_template = f.read()

# Setup socket
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
    else:
        html = html_template # If you still use %s for table, otherwise ignore
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.sendall(html)

    cl.close()
