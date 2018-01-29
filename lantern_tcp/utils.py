import asyncio
from collections import defaultdict
import struct


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


class TCPClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def data_received(self, data: bytes):
        """
        Get data and execute commands
        """
        for command_code, value in self.parse_tlv(data):
            self.execute(command_code, value)

    def parse_tlv(self, data: bytes):
        """
        Parse and yield TLV-commands from data buffer
        """
        start = 0
        while True:
            tmp = data[start:]
            if not tmp:
                break
            
            try:
                command_code, length = struct.unpack('>BH', tmp[:3])
                value = None
                if length > 0:
                    value = struct.unpack(f'>{length}s', tmp[3:length+3])[0]
                yield command_code, value
                start += length + 3
            except struct.error:
                break

    def execute(self, command_code, value):
        """
        Find and execute device command by its code
        """
        class_commands = cmd.commands[self.__class__.__name__]
        if command_code in class_commands:
            method = class_commands[command_code]
            args = []
            if value is not None:
                args.append(value)
            method(self, *args)

    def connection_lost(self, exc):
        self.loop.stop()
