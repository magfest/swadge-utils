#!/usr/bin/env python3

import threading
import random
import socket
import struct
import time
import sys

from proto import BUTTON_IDS, BUTTON_NAMES, button_bit
from proto.udp import MacAddress, ScanRequestPacket, ScanPacket, StatusPacket, LightsPacket, LightsRssiPacket

from common import colors


class StoppedException(Exception):
    pass


class Badge:
    @staticmethod
    def random_mac():
        return MacAddress(bytes([random.getrandbits(8) for _ in range(6)]))

    @staticmethod
    def random_stations():
        return [
            {'bssid': str(Badge.random_mac()), 'rssi': random.randint(-128, 127), 'channel': random.randint(1, 14)}
            for _ in range(random.randint(0, 47))
        ]

    def __init__(self, version=1, mac=None, server_host='magbadge.me', server_port=8000, receive=False):
        self.server_host = server_host
        self.server_port = server_port
        self.mac = MacAddress(mac) if mac else Badge.random_mac()

        self._receive = receive
        self._recv_thread = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.version = version
        self._rssi = -128
        self.connected_bssid = MacAddress(0)
        self.gpio_state = 0
        self.gpio_trigger = 0
        self.gpio_down = 0
        self.led_power = 0
        self.battery_voltage = 255
        self.update_id = 0
        self.heap_free = 65535
        self.sleep_performance = 255
        self.scan_pending = False

        self.running = False

        self._epoch = int(time.time())

    def button_press(self, name):
        if name not in BUTTON_IDS:
            raise ValueError("Invalid button name '{}'".format(name))

        self.gpio_down = 1
        self.gpio_trigger = BUTTON_IDS[name]
        self.gpio_state |= button_bit(BUTTON_IDS[name])
        self.send_update()
        self.gpio_down = 0
        self.gpio_trigger = 0

    def button_release(self, name):
        if name not in BUTTON_IDS:
            raise ValueError("Invalid button name '{}'".format(name))

        self.gpio_down = 0
        self.gpio_trigger = BUTTON_IDS[name]
        self.gpio_state &= (0xff ^ button_bit(BUTTON_IDS[name]))
        self.send_update()
        self.gpio_trigger = 0

    @property
    def rssi(self):
        return self._rssi or random.randint(-128, 127)

    def send_packet(self, packet):
        self.sock.sendto(bytes(self.mac) + packet.to_bytes(), (self.server_host, self.server_port))

    def send_update(self):
        self.send_packet(StatusPacket(
            self.version,
            self.rssi,
            bytes(self.connected_bssid),
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

    def send_scan(self):
        self.send_packet(ScanPacket(int(time.time()), Badge.random_stations()))

    @property
    def time(self):
        return int(time.time()) - self._epoch

    @property
    def mac_str(self):
        return str(self.mac)

    @property
    def mac_int(self):
        return int(self.mac)

    def stop(self):
        self.running = False

    def sleep(self, length):
        if not self.running:
            raise StoppedException()

        if length > 5:
            time.sleep(5)

            self.sleep(length - 5)
        else:
            time.sleep(length)

    def on_lights(self, packet):
        if packet.matches_mac(self.mac):
            color_names = [colors.color_name(colors.Color(c).rgb) for c in packet.colors]
            print("{!s}: LIGHTS [{:^11s}] [{:^11s}] [{:^11s}] [{:^11s}]".format(self.mac, *color_names))

    def on_scan_request(self):
        self.scan_pending = True

    def on_lights_rssi(self, packet):
        pass

    def listen(self):
        self.sock.bind(('0.0.0.0', 8001))
        self.sock.settimeout(10)

        buf = bytearray(1024)
        while self.running:
            try:
                count = self.sock.recv_into(buf, 1024)

                if count >= 7:
                    mac = buf[0:6]
                    kind = buf[6]
                    rest = buf[6:count]

                    if bytes(self.mac) != mac:
                        continue

                    if kind == LightsPacket.ID:
                        self.on_lights(LightsPacket.from_bytes(rest))
                    elif kind == ScanRequestPacket.ID:
                        self.on_scan_request()
                    elif kind == LightsRssiPacket.ID:
                        self.on_lights_rssi(LightsRssiPacket.from_bytes(rest))
                else:
                    print("Discarding invalid packet")
            except socket.timeout:
                # This is fine
                pass

    def run(self):
        self.running = True

        if self._receive:
            self._recv_thread = threading.Thread(target=self.listen)
            self._recv_thread.start()

        self.send_update()

        try:
            #self.sleep(random.randrange(30))
            print("{!s}: Initialized".format(self.mac))

            while self.running:
                self.send_update()
                #self.sleep(5)

                if self.scan_pending:
                    self.send_scan()
                    self.scan_pending = False

                if random.randrange(5) > 2:
                    button = random.choice(list(BUTTON_NAMES.values()))
                    self.button_press(button)
                    self.sleep(.5)
                    self.button_release(button)
                    self.sleep(4.5)
                else:
                    self.sleep(5)

        except StoppedException:
            pass

        if self._recv_thread:
            self._recv_thread.join()


if __name__ == "__main__":
    badge_count = 1

    if len(sys.argv) > 1:
        badge_count = int(sys.argv[1])

    if len(sys.argv) > 2:
        random.seed(int(sys.argv[2]))

    receive = False
    if len(sys.argv) > 3:
        receive = True

    print("Simulating {} badges!".format(badge_count))

    badges = [Badge(version=1, receive=receive) for _ in range(badge_count)]
    threads = [threading.Thread(target=b.run) for b in badges]

    for thread in threads:
        thread.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Waiting for {} badges to stop...".format(badge_count))

        for badge in badges:
            badge.stop()

        for thread in threads:
            thread.join()
