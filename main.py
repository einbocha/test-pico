import network, uasyncio as asyncio
import time
import ujson
import urequests
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# I2C setup (default pins GP4=SDA, GP5=SCL for Pico I2C0)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# Scan and print I2C devices (should show 0x3C)
# print('I2C devices:', [hex(addr) for addr in i2c.scan()])

oled = SSD1306_I2C(128, 32, i2c)

SSID = ""
PASSWORD = ''

# Wi-Fi connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(SSID, PASSWORD)

print('Connecting to', SSID)
while not wlan.isconnected():
    time.sleep(1)
    print('.', end='')

print('\nIP:', wlan.ifconfig()[0])


STATE = '/state.json'


def write_state(state):
    try:
        with open(STATE, 'w') as f:
            f.write(ujson.dumps(state))

        print(f'Saved state')
    except Exception as e:
        print('Write error:', e)


def read_state():
    try:
        with open(STATE, 'r') as f:
            return ujson.loads(f.read())
    except Exception as e:
        print('Read error:', e)
        return None


if not read_state():
    write_state({
        'state': [],
    })


async def personal_state():
    while True:
        try:
            response = urequests.get(
                'http://einbocha.ch:8000/',
                auth=('', '')
            )

            data = ujson.loads(response.text)

            print(data)

            write_state(data)

            response.close()

        except Exception as e:
            print('HTTP error:', e)

        await asyncio.sleep(21)


async def display_state():
    while True:
        state = read_state()

        messages = state['state']

        old = ''
        for msg in messages:
            if len(msg) > 16:
                old = msg[:16]
            oled.fill(0)
            oled.text(old, 0, 0)
            oled.text(msg, 0, 20)
            oled.show()
            old = msg
            await asyncio.sleep(5)


async def main():
    asyncio.create_task(personal_state())
    asyncio.create_task(display_state())

    while True:
        await asyncio.sleep(1)

asyncio.run(main())
