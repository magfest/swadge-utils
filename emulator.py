#!/usr/bin/env python3

from common.swadge import Swadge
from transport import udp, wamp
from interface import text
import functools
import threading
import optparse
import time

# All badges should recalculate every 1/100th of a second
TICK_RATE = 0.01


class Simulator:
    def __init__(self, interface, transport, environment, count, thread_count=1):
        self.interface = interface
        self.transport = transport
        self.environment = environment
        self.count = count

        self.thread_count = thread_count

        self._interface_thread = None

        self._running = False

    def stop(self):
        self._running = False

    def run_thread(self, thread_index):
        badges = [Swadge(transport=self.transport,
                         interface=self.interface,
                         environment=self.environment)
                  for _ in range(thread_index, self.count, self.thread_count)]

        next_loop = 0
        self._running = True
        while self._running:
            cur_loop = time.time()
            next_loop = cur_loop + .01

            for badge in badges:
                badge.loop(cur_loop)

            diff = next_loop - time.time()
            if diff > 0:
                time.sleep(diff)

    def run(self):
        self._interface_thread = threading.Thread(target=self.interface.run)
        self._interface_thread.start()

        threads = [threading.Thread(target=functools.partial(self.run_thread, i))
                                    for i in range(self.thread_count)]

        for t in threads:
            t.start()

        self.transport.run()

        for t in threads:
            t.join()


if __name__ == "__main__":
    parser = optparse.OptionParser(usage="usage: %prog [options] [url]")
    parser.add_option("-c", "--count", dest="count", help="simulate COUNT badges", metavar="COUNT",
                      default=1)
    parser.add_option("-i", "--interface", dest="interface", help="set the badge interface to use",
                      default="text")
    parser.add_option("-t", "--transport", dest="transport", default="wamp",
                      help="set the transport mode to use, either 'udp' or 'wamp'")
    parser.add_option("-e", "--environment", dest="environment",
                      help="set the environment simulator to use")
    parser.add_option("-j", "--threads", dest="threads",
                      help="set the number of threads to use", default=1)
    (options, args) = parser.parse_args()

    transport, interface, environment = None, None, None

    if options.transport == "udp":
        host, port = args[0].split(":") if args else ("api.swadge.com", 1337)
        transport = udp.UdpTransport(host, int(port))
    elif options.transport == "wamp":
        url = args[0] if args else "ws://api.swadge.com:1337/ws"
        transport = wamp.WampTransport(url)

    if options.interface == "text":
        interface = text.Interface()

    if options.environment == "random":
        environment = None

    sim = Simulator(interface=interface, transport=transport, environment=environment,
                    count=options.count, thread_count=options.threads)

    try:
        sim.run()
    except InterruptedError:
        print("Waitign for simulator to exit...")
        sim.stop()
