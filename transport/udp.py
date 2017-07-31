#!/usr/bin/env python3

import random
import socket
import sys
import threading
import time

from common import colors, MacAddress
from proto import BUTTON_IDS, BUTTON_NAMES, button_bit
from proto.packet import ScanRequestPacket, ScanPacket, StatusPacket, LightsPacket, \
    LightsRssiPacket


class UdpTransport:
    def __init__(self, host, port):
        self.badges = {}

        self.server_host = host
        self.server_port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self._recv_thread = None

    def stop(self):
        self.running = False

    def register_badge(self, badge):
        self.badges[badge.mac] = badge

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

                    badge = self.badges.get(int(MacAddress(mac)), None)
                    if badge:
                        if kind == LightsPacket.ID:
                            badge.on_lights(LightsPacket.from_bytes(rest))
                        elif kind == ScanRequestPacket.ID:
                            badge.on_scan_request()
                        elif kind == LightsRssiPacket.ID:
                            badge.on_lights_rssi(LightsRssiPacket.from_bytes(rest))
                else:
                    print("Discarding invalid packet")
            except socket.timeout:
                # This is fine
                pass

    def send_packet(self, mac, packet):
        self.sock.sendto(bytes(mac) + packet.to_bytes(), (self.server_host, self.server_port))
