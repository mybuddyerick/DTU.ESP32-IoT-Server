from machine import I2C
from micropython import const

# Default I2C address and register for temperature reading.
_MCP9808_DEFAULT_ADDRESS = const(0x18)
_MCP9808_REG_TEMP = const(0x05)

class MCP9808:
    def __init__(self, i2c: I2C, address: int = _MCP9808_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address

    def read_temperature(self) -> float:
        # Read 2 bytes from the temperature register.
        data = self.i2c.readfrom_mem(self.address, _MCP9808_REG_TEMP, 2)
        # Combine the two bytes.
        raw = (data[0] << 8) | data[1]
        # Extract the lower 12 bits.
        temp = raw & 0x0FFF
        # Multiply by resolution to get Celsius.
        temp_c = temp * 0.0625
        # If the sign bit is set, subtract 256 to get negative temperature.
        if raw & 0x1000:
            temp_c -= 256
        return temp_c

    @property
    def temperature(self) -> float:
        return self.read_temperature()
