import re
import struct


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

    def __eq__(self, other):
        if isinstance(other, MacAddress):
            return other._bytes == self._bytes
        else:
            return MacAddress(other)._bytes == self._bytes

    def __int__(self):
        return struct.unpack('>Q', b'\x00\x00' + self._bytes)[0]

    def __str__(self):
        return MacAddress.bytes_to_str(self._bytes)

    def __bytes__(self):
        return self._bytes
