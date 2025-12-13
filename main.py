import network, time, requests, ujson, machine
import config


class RobotClient:
    def __init__(self, wifi, server):
        self.wifi_ssid = wifi['ssid']
        self.wifi_pwd = wifi['pwd']
        self.server_url = f'http://www.{server['hostname']}:{server['port']}'
        self.wlan = network.WLAN(network.STA_IF)
        self.connect_wifi()

    def connect_wifi(self):
        ssid = self.wifi_ssid
        password = self.wifi_pwd
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        print('Connecting to', ssid)
        while not self.wlan.isconnected():
            time.sleep(1)
            print('.', end='')
        print('\nWiFi connected:', self.wlan.ifconfig())

    def get_status(self):
        try:
            resp = requests.get(self.server_url + '/status')
            data = ujson.loads(resp.text)
            resp.close()
            print('Status:', data)
            return data
        except Exception as e:
            print('GET error:', e)
            return None

    def send_telemetry(self, sensors):
        try:
            data = {"sensors": sensors, "timestamp": time.ticks_ms()}
            resp = requests.post(self.server_url + '/telemetry', json=data)
            print('Telemetry OK:', resp.status_code)
            resp.close()
        except Exception as e:
            print('POST error:', e)

    def send_command(self, cmd):
        try:
            data = {"command": cmd}
            resp = requests.post(self.server_url + '/command', json=data)
            print('Command sent:', resp.status_code)
            resp.close()
        except Exception as e:
            print('Command error:', e)


# Usage loop for your robot
client = RobotClient(config.wifi, config.server)
while True:
    client.get_status()
    client.send_telemetry({"lidar": 150, "battery": 82})
    time.sleep(5)
