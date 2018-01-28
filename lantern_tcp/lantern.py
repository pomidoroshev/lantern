"""
Lantern TCP Client
"""

import argparse
import asyncio
import time

from xtermcolor import colorize

from .settings import HOST, PORT, SLEEPTIME_RECONNECT
from .utils import cmd, TCPClientProtocol


class LanternProtocol(TCPClientProtocol):
    """
    Lantern protocol with set of commands:
    0x12 - turn lantern on
    0x13 - turn lantern off
    0x20 - change lantern color

    Lantern is on and red by default
    """

    _is_on = True
    _color_rgb = 0xff0000

    def __init__(self, loop):
        super().__init__(loop)
        self.refresh()

    def refresh(self):
        """
        Print new lantern icon with current parameters
        """
        if self._is_on:
            print(colorize('\u2B24', rgb=self._color_rgb))
        else:
            print('\u2B55')

    @cmd(0x12)
    def on(self):
        """
        Turn lantern on
        """
        self._is_on = True
        self.refresh()

    @cmd(0x13)
    def off(self):
        """
        Turn lantern off
        """
        self._is_on = False
        self.refresh()

    @cmd(0x20)
    def color(self, value: bytes):
        """
        Change lantern color
        """
        value = int.from_bytes(value, byteorder='big')
        self._color_rgb = value
        self.refresh()


def main():
    parser = argparse.ArgumentParser(description='Lantern TCP Client')
    parser.add_argument('host', type=str, default=HOST, nargs='?',
                        help='Server host, default is %(default)s')
    parser.add_argument('port', type=int, default=PORT, nargs='?',
                        help='Server port, default is %(default)s')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    while True:
        try:
            coro = loop.create_connection(lambda: LanternProtocol(loop),
                                          args.host, args.port)
            loop.run_until_complete(coro)
            loop.run_forever()
        except OSError:
            print('Reconnecting in 1 second...')
            time.sleep(SLEEPTIME_RECONNECT)

    loop.close()


if __name__ == '__main__':
    main()
