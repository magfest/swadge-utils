import time

from common import colors, MacAddress
from proto import VERSION_2017_LABS, BUTTON_IDS, button_bit
from proto.packet import StatusPacket, ScanPacket

# How often to send statuses
STATUS_FREQ = 10
SCAN_MAX_STATIONS = 140

# The number of ticks per second, approximately. On real badges this varies, a lot.
TIME_FACTOR = 1750000

class Swadge:
    def __init__(self, version=VERSION_2017_LABS, mac=0,
                 transport=None, interface=None, environment=None):
        """
        Simulates a swadge!
        :param version:     The hardware version to emulate
        :param mac:         The MAC Address or ID of this swadge
        :param transport:   Simulates network transport and handles sending and receiving packets
        :param interface:   Handles physical attributes such as light display and button presses
        :param environment: Supplies environmental information such as RSSI and connected station
        """
        self.transport = transport
        self.interface = interface
        self.environment = environment

        self.mac = MacAddress(mac)

        self.version = version
        self.rssi = -128
        self.connected_bssid = MacAddress(0)
        self.gpio_state = 0
        self.gpio_trigger = 0
        self.gpio_down = 0
        self.battery_voltage = 255

        self.update_id = 0
        self.heap_free = 65535
        self.sleep_performance = 255
        self.scan_pending = False

        self.running = False

        # grb, grb, grb, grb
        self.last_lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.light_stack = [[], [], [], []]
        self._pending_packets = []
        self._pending_update = True

        self._epoch = time.time()
        self._last_status_time = 0.0
        self._lights_pending = False

        if interface:
            interface.register_badge(self)

        if transport:
            transport.register_badge(self)

    def send_packet(self, packet):
        if self.transport:
            self.transport.send_packet(self.mac, packet)
        else:
            print("Sent packet")

    def send_scan(self, scan):
        self.send_packet(scan)

    def send_update(self):
        self.send_packet(StatusPacket(
            self.version,
            self.rssi,
            self.connected_bssid,
            self.gpio_state,
            self.gpio_trigger,
            self.gpio_down,
            self.led_power,
            self.battery_voltage,
            self.update_id,
            self.heap_free,
            self.sleep_performance,
            self.time
        ))
        self.update_id += 1

    def show_lights(self, c1, c2, c3, c4):
        if self.interface:
            self.interface.show_lights(int(self.mac), c1, c2, c3, c4)
        else:
            color_names = [colors.color_name(colors.Color(c).rgb) for c in packet.colors]
            print("{!s}: LIGHTS [{:^11s}] [{:^11s}] [{:^11s}] [{:^11s}]".format(self.mac, *color_names))

    def led_power(self):
        return sum(self.last_lights) // 12

    def loop(self, timestamp):
        if self.gpio_trigger \
                or self._pending_update \
                or self._last_status_time + STATUS_FREQ <= timestamp:

            self.rssi = self.environment.get_rssi() if self.environment else -65
            self.connected_bssid = self.environment.get_station() if self.environment else MacAddress()
            self.sleep_performance = 128

            # We don't accurately simulate only updating sleep performance at long intervals
            self.send_packet(StatusPacket(
                self.version,
                self.rssi,
                self.connected_bssid,
                self.gpio_state,
                self.gpio_trigger,
                self.gpio_down,
                self.led_power(),
                self.battery_voltage,
                self.update_id,
                self.heap_free,
                self.sleep_performance,
                self.time))

            self.update_id += 1
            self._last_status_time = time.time()

            self._pending_update = False
            self.gpio_trigger = 0

        if self._lights_pending:
            self.show_lights(*self.last_lights)

        if self.scan_pending and self._last_status_time + .1 <= timestamp:
            self.scan_pending = False

            stations = self.environment.get_scan()

            scan_id = self.time
            # Send multiple packets if needed
            for i in range(0, len(stations), SCAN_MAX_STATIONS):
                self.send_scan(ScanPacket(scan_id, stations[i:i+SCAN_MAX_STATIONS]))

    @property
    def time(self):
        return int((time.time() - self._epoch) * TIME_FACTOR)

    def on_button_press(self, name):
        if name not in BUTTON_IDS:
            raise ValueError("Invalid button name '{}'".format(name))

        self.gpio_down = 1
        self.gpio_trigger = BUTTON_IDS[name]
        self.gpio_state |= button_bit(BUTTON_IDS[name])

    def on_button_release(self, name):
        if name not in BUTTON_IDS:
            raise ValueError("Invalid button name '{}'".format(name))

        self.gpio_down = 0
        self.gpio_trigger = BUTTON_IDS[name]
        self.gpio_state &= (0xff ^ button_bit(BUTTON_IDS[name]))

    def stop(self):
        self.running = False

    def on_lights(self, packet):
        if packet.matches_mac(self.mac):
            pass

    def on_scan_request(self):
        self.scan_pending = True

    def on_lights_rssi(self, packet):
        pass
