from os import environ
import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import SubscribeOptions
from autobahn.wamp import auth
from proto import BUTTON_NAMES
from proto.packet import StatusPacket, ScanPacket, LightsPacket
import time


class _WampSession(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.badges = {}
        try:
            self.loop = asyncio.get_event_loop()
        except:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def onConnect(self):
        self.join("swadges", ["wampcra"], "simulator")

    def onChallenge(self, challenge):
        if challenge.method == u"wampcra":
            signature = auth.compute_wcs(u"icantbelieveitsnotabadge".encode('utf8'),
                                         challenge.extra['challenge'].encode('utf8'))
            return signature.decode('ascii')
        else:
            raise Exception("don't know how to handle authmethod {}".format(challenge.method))

    def onDisconnect(self):
        self.loop.stop()

    def stop(self):
        self.loop.stop()

    async def _do_register_badge(self, badge_id):
        badge_prefix = u'badge' + str(badge_id)
        await self.subscribe(self.on_lights, badge_prefix + u'.lights_static')
        await self.subscribe(self.on_request_scan, badge_prefix + u'.request_scan')
        # TODO RSSI

    def register_badge(self, badge):
        self.badges[int(badge.mac)] = badge
        self.loop.run_until_complete(self._do_register_badge(int(badge.mac)))

    def send_packet(self, mac, packet):
        if packet.ID == StatusPacket.ID:
            if packet.gpio_trigger:
                state = 'press' if packet.gpio_down else 'release'
                self.publish('badge.' + str(int(mac)) + '.button.' + state,
                             [BUTTON_NAMES[packet.gpio_trigger]],
                             {"badge_id": int(mac), "timestamp": int(time.time() * 1000)})
        elif packet.ID == ScanPacket.ID:
            self.publish('badge.' + str(int(mac)) + '.scan', [],
                         {"badge_id": int(mac),
                          "timestamp": int(time.time() * 1000),
                          "stations": packet.stations})

    async def on_lights(self, c0, c1, c2, c3, match=0, mask=0, details=None):
        _, badge_id, __ = details.topic.split('.')
        badge = self.badges.get(int(badge_id), None)

        if badge:
            badge.on_lights(LightsPacket(match, mask, c0, c1, c2, c3))

    async def on_request_scan(self, *args, details=None, **kwargs):
        _, badge_id, __ = details.topic.split('.')
        badge = self.badges.get(int(badge_id), None)

        if badge:
            badge.on_request_scan()


class WampTransport:
    def __init__(self, url, realm="swadges"):
        self.url = url
        self.realm = realm

        self._transport = None

    def send_packet(self, *args, **kwargs):
        if self._transport:
            return self._transport.send_packet(*args, **kwargs)

    def register_badge(self, *args, **kwargs):
        if self._transport:
            return self._transport.register_badge(*args, **kwargs)

    def stop(self):
        if self._transport:
            self._transport.stop()

    def get_transport(self, cfg):
        self._transport = _WampSession(cfg)
        return self._transport

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        runner = ApplicationRunner(
            self.url,
            self.realm
        )

        runner.run(self.get_transport, log_level='info')
