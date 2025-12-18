from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# I2C setup (default pins GP4=SDA, GP5=SCL for Pico I2C0)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# Scan and print I2C devices (should show 0x3C)
print('I2C devices:', [hex(addr) for addr in i2c.scan()])

oled = SSD1306_I2C(128, 32, i2c)

# Test display
oled.fill(0)  # Clear screen
oled.text('Test', 0, 0)
oled.show()

time.sleep(3)

# Scroll demo
while True:
    oled.scroll(2, 0)  # Horizontal scroll
    time.sleep(1)
    oled.show()
