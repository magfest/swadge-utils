import struct

from common import MacAddress


class StatusPacket:
    ID = 0x01

    def __init__(self,
                 version,
                 rssi,
                 connected_bssid,
                 gpio_state,
                 gpio_trigger,
                 gpio_down,
                 led_power,
                 battery_voltage,
                 update_id,
                 heap_free,
                 sleep_performance,
                 timestamp):
        self.version = version
        self.rssi = rssi
        self.connected_bssid = connected_bssid
        self.gpio_state = gpio_state
        self.gpio_trigger = gpio_trigger
        self.gpio_down = gpio_down
        self.led_power = led_power
        self.battery_voltage = battery_voltage
        self.update_id = update_id
        self.heap_free = heap_free
        self.sleep_performance = sleep_performance
        self.timestamp = timestamp

    @classmethod
    def from_bytes(cls, val):
        pass

    def to_bytes(self):
        return struct.pack(">3B6s4B3HBI",
                           StatusPacket.ID, self.version, self.rssi + 128,
                           self.connected_bssid,
                           self.gpio_state,
                           self.gpio_trigger,
                           self.gpio_down,
                           self.led_power,
                           self.battery_voltage,
                           self.update_id,
                           self.heap_free,
                           self.sleep_performance,
                           self.timestamp)


class LightsPacket:
    ID = 0x02

    @staticmethod
    def hex_to_grb(num):
        return (num >> 8) & 0xff, (num >> 16) & 0xff, num & 0xff

    @staticmethod
    def grb_to_hex(g, r, b):
        return (r & 0xff) << 16 | (g & 0xff) << 8 | (b & 0xff)

    def __init__(self, match, mask, c1, c2, c3, c4):
        self.match = match
        self.mask = mask

        self.colors = [c1, c2, c3, c4]

    @classmethod
    def from_bytes(cls, val):
        packet_id, match, mask, *color_bytes = struct.unpack(">BBBx12B", val)

        assert(packet_id == LightsPacket.ID)

        grb_colors = zip(*(iter(color_bytes),) * 3)
        hex_colors = [LightsPacket.grb_to_hex(*c) for c in grb_colors]

        return LightsPacket(match, mask, *hex_colors)

    def to_bytes(self):
        return struct.pack(">BBBx12B", LightsPacket.ID, self.match, self.mask,
                           *sum((LightsPacket.hex_to_grb(c) for c in self.colors), ()))

    def matches_mac(self, mac: MacAddress):
        return not ((bytes(mac)[-1] ^ self.match) & self.mask)


class LightsRssiPacket:
    ID = 0x03


class ScanRequestPacket:
    ID = 0x04

    def to_bytes(self):
        return bytes([ScanRequestPacket.ID])

    @classmethod
    def from_bytes(cls, val):
        return ScanRequestPacket()


class ScanPacket:
    ID = 0x05

    def __init__(self, timestamp, stations):
        self.timestamp = timestamp
        self.stations = stations

        if len(stations) > 47:
            raise ValueError("Too many stations, invalid packet")

    def to_bytes(self):
        return struct.pack(">BIB", ScanPacket.ID, self.timestamp, len(self.stations)) \
               + b''.join((struct.pack(">6sBB", bytes(station['bssid']), station['rssi'] + 128, station['channel'])
                           for station in self.stations))
