import struct
import re


class MacAddress:
    @staticmethod
    def bytes_to_str(byte_val):
        if len(byte_val) != 6:
            raise ValueError("Not a valid MAC address")

        return ':'.join(('{:02X}'.format(b) for b in byte_val))

    @staticmethod
    def normalize_str(str_val):
        cleaned = re.sub(r'[^0-9A-F]', '', str_val.upper())

        if len(cleaned) != 12:
            raise ValueError("Not a valid MAC address")

        return ':'.join(a + b for a, b in zip(cleaned[0::2], cleaned[1::2]))

    @staticmethod
    def str_to_bytes(str_val):
        return bytes([int(n, 16) for n in MacAddress.normalize_str(str_val).split(':')])

    def __init__(self, val=None):
        if isinstance(val, str):
            self._bytes = MacAddress.str_to_bytes(val)
        elif isinstance(val, bytes):
            self._bytes = val
        elif isinstance(val, int):
            self._bytes = bytes([(val >> n) & 0xff for n in range(40, -1, -8)])
        else:
            self._bytes = bytes(6)

    def __int__(self):
        return struct.unpack('>Q', b'\x00\x00' + self._bytes)[0]

    def __str__(self):
        return MacAddress.bytes_to_str(self._bytes)

    def __bytes__(self):
        return self._bytes


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
