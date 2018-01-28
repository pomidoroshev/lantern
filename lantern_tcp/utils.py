import asyncio

from collections import defaultdict


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
    """
    Base class for manageable devices
    """
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
