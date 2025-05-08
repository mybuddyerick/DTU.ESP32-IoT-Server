<div align="center">
  <img src="https://github.com/user-attachments/assets/9ea39d49-e732-4c1a-9bd7-f9d72f1e6d4d" alt="Logo" height="140">
</div>

<h1 align="center">02135 Introduction to Cyber Systems - ESP32 IoT Web Server Project</h1>

This project implements a simple **Internet-of-Things (IoT)** node using an **Adafruit Feather Huzzah32 (ESP32)** board and **MicroPython**.  
It serves a **web dashboard** to monitor sensors and control outputs remotely, using **WiFi** communication and a **Web API** with **JSON** responses.

Project completed as part of **Assignment 4** in the course *02135 - Introduction to Cyber Systems* (Spring 2025).

---

## Setup and How to Use

1. **Upload all project files** (`main.py`, `engine.py`, `mcp9808.py`, `index.html`, `style.css`, `updater.js`) with Pymakr.
2. **Power the ESP32** and connect to its WiFi network:
   - SSID: `mini-Markus`
   - Password: `ra2ra2ra2`
3. **Open a web browser** and go to:  
   ➔ [`http://192.168.4.1`](http://192.168.4.1)
4. **Dashboard Overview**:
   - Real-time temperature display.
   - Potentiometer visualization.
   - Button 1 visual representation.
   - Pin configuration table.
   - Interactive button to toggle the RGB LED.

---

## Project Structure

| File | Purpose |
|:----|:--------|
| `main.py` | Starts the WiFi server, listens for HTTP requests, routes API endpoints. |
| `engine.py` | Handles hardware interactions: sensors, button, RGB LED control. |
| `mcp9808.py` | Library for the MCP9808 temperature sensor. |
| `index.html` | Web dashboard front-end. |
| `style.css` | Dashboard styling. |
| `updater.js` | Periodically updates sensor readings and manages dashboard interactions. |

---

## Tasks

### Task 1: WiFi Web Server Setup
- Configured the ESP32 as a **WiFi access point**.
- Implemented a basic **HTTP server**.
- Served an **HTML dashboard** displaying sensor values.

### Task 2: Display Inputs and Sensors
- Extended the dashboard to show:
  - Temperature readings.
  - Potentiometer position.
  - Button 1 press state.
  - Pin statuses.
- Real-time updating using **AJAX** (JavaScript `fetch`) every 200 milliseconds.

### Task 3: Web API Implementation (JSON Responses)
- Created a **REST-style Web API** serving **JSON**-encoded data.
- Supported endpoints:
  | Endpoint | Description |
  |:---------|:------------|
  | `/api/data` | All data (temperature, potentiometer, button, pins, RGB). |
  | `/api/pins` | List of all pins and their current values. |
  | `/api/temperature` | Current temperature. |
  | `/api/potentiometer` | Current potentiometer value. |
  | `/api/button1` | Button 1 state (0 or 1). |
  | `/api/rgb` | Current RGB LED brightness levels. |

- Explained and used **JSON** format for efficient machine-readable communication.

Example response (`/api/temperature`):
```json
{
  "temperature": 26.5
}
```

### Task 4: Remote Hardware Control via Web API
- Added **control endpoint** `/api/toggle`:
  - Remotely toggles the RGB LED ON/OFF.
- Clicking the dashboard's center button sends a `GET` request to `/api/toggle`.
- The ESP32 toggles the LED similarly to a physical button press.

---

## Web API Endpoints

| Path | Purpose | Response |
|:----|:--------|:---------|
| `/api/data` | All sensor and pin data | JSON |
| `/api/pins` | Pin configurations and values | JSON |
| `/api/temperature` | Current temperature reading | JSON |
| `/api/potentiometer` | Potentiometer value | JSON |
| `/api/button1` | Button 1 state (0 = not pressed, 1 = pressed) | JSON |
| `/api/rgb` | RGB LED brightness values | JSON |
| `/api/toggle` | Toggle RGB LED state | Plain text ("LED toggled") |

---

## Features

- **Real-time updates** (no page reload needed).
- **Clean and styled dashboard**.
- **Modular API design** (extensible for future endpoints).
- **Two-way communication**:
  - Sensor reading.
  - Remote hardware control.

---

## Technical Requirements

- **Board:** Adafruit Feather Huzzah32 (ESP32)
- **Language:** MicroPython
- **Libraries Used:** `network`, `socket`, `machine`, `ujson`, `I2C`, `PWM`, `ADC`

---

## Summary

- Setting up a WiFi server on embedded hardware (ESP32).
- Designing and handling raw HTTP requests manually without using a full web framework.
- Using JSON as an efficient, machine-readable communication format.
- Creating a RESTful Web API for modular data and command handling.
- Controlling hardware outputs remotely via HTTP requests.
- Building a dynamic, real-time web dashboard using JavaScript (AJAX fetch) to update sensor data without refreshing the page.
- Styling a responsive and user-friendly website using CSS, including custom designs for buttons, progress bars, and tables.
- Integrating front-end technologies (HTML, CSS, JavaScript) with back-end MicroPython services for a complete IoT solution.

---

# How to Test

1. Connect to the ESP32 WiFi (`mini-Markus`).
2. Visit `http://192.168.4.1`.
3. Interact with the dashboard:
   - Watch live temperature and potentiometer updates.
   - Click the dashboard button to toggle the RGB LED.
4. Test API directly:
   - Visit `http://192.168.4.1/api/temperature` for current temperature.
   - Visit `http://192.168.4.1/api/pins` for pin status.

---

# Authors
- **Markus Lassen**
- **Eirik Sigurstein**
- **Karl Lankots**
- *02135 - Introduction to Cyber Systems, Spring 2025*
