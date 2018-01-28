"""
Lantern TCP Client
"""

import argparse
import asyncio

from xtermcolor import colorize

from utils import cmd, Manageable


class Lantern(Manageable):
    """
    Lantern class with set of commands:
    0x12 - turn lantern on
    0x13 - turn lantern off
    0x20 - change lantern color

    Lantern is on and red by default
    """

    def __init__(self, is_on=True, color=0xff0000):
        self._is_on = is_on
        self._color_rgb = color

    async def listen(self, *args, **kwargs):
        """
        Show current lantern state berore listen
        """
        self.refresh()
        await super().listen(*args, **kwargs)

    def refresh(self):
        """
        Print new lantern icon with current parameters
        """
        if self._is_on:
            print(colorize('\u2B24', rgb=self._color_rgb))
        else:
            print('\u2B55')

    @cmd(0x12)
    async def on(self):
        """
        Turn lantern on
        """
        self._is_on = True
        self.refresh()

    @cmd(0x13)
    async def off(self):
        """
        Turn lantern off
        """
        self._is_on = False
        self.refresh()

    @cmd(0x20)
    async def color(self, value: bytes):
        """
        Change lantern color
        """
        value = int.from_bytes(value, byteorder='big')
        self._color_rgb = value
        self.refresh()


def main():
    loop = asyncio.get_event_loop()
    lantern = Lantern()

    parser = argparse.ArgumentParser(description='Lantern TCP Client')
    parser.add_argument('host', type=str, default='127.0.0.1', nargs='?',
                        help='Server host, default is %(default)s')
    parser.add_argument('port', type=int, default=9999, nargs='?',
                        help='Server port, default is %(default)s')
    args = parser.parse_args()
    loop.run_until_complete(lantern.listen(args.host, args.port, loop=loop))


if __name__ == '__main__':
    main()
