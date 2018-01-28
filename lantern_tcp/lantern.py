import argparse
import asyncio
from collections import defaultdict
from functools import wraps

from xtermcolor import colorize


def cmd(code):
    """
    Collect commands from class methods
    """
    if not hasattr(cmd, 'commands'):
        cmd.commands = defaultdict(dict)

    def _cmd(fn):
        classname = fn.__qualname__.split('.')[0]
        cmd.commands[classname][code] = fn
        return fn

    return _cmd


class Manageable:

    async def listen(self, host, port, *, loop):
        """
        Connect to server and listen to commands
        """
        reader, _ = await asyncio.open_connection(host, port, loop=loop)
        while True:
            await self.execute_command(reader)

    async def execute_command(self, reader):
        """
        Execute class command
        """
        type_, value = await self.get_tlv(reader)
        command_code = ord(type_)
        class_commands = cmd.commands[self.__class__.__name__]
        if command_code in class_commands:
            method = class_commands[command_code]
            args = []
            if value is not None:
                args.append(value)
            await method(self, *args)

    async def get_tlv(self, reader):
        """
        Parse TLV-command and get type and value
        """
        type_ = await reader.read(1)
        if type_:
            value = None
            length = await reader.read(2)
            length = int.from_bytes(length, byteorder='big')
            if length > 0:
                value = await reader.read(length)
            return type_, value


class Lantern(Manageable):
    """
    Lantern class
    """

    def __init__(self, is_on=True, color=0xff0000):
        self._is_on = is_on
        self._color_rgb = color

    async def listen(self, *args, **kwargs):
        self.refresh()
        await super().listen(*args, **kwargs)

    def refresh(self):
        if self._is_on:
            print(colorize('\u2B24', rgb=self._color_rgb))
        else:
            print('\n')

    @cmd(0x12)
    async def on(self):
        """
        Turn lantern on
        """
        self._is_on = True
        print('Lantern is on...')
        self.refresh()

    @cmd(0x13)
    async def off(self):
        """
        Turn lantern off
        """
        self._is_on = False
        print('Lantern is off...')
        self.refresh()

    @cmd(0x20)
    async def color(self, value: bytes):
        """
        Switch lantern color
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
