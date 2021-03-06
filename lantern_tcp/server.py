"""
Demo-server for lantern
"""

import argparse
import asyncio

from .settings import HOST, PORT


class LanternServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        """
        Wait for lantern connection and send some commands
        """
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        print('Connection from', self.peername)

        commands = [
            # Turn off
            bytearray([0x13, 0x00, 0x00]),

            # Turn on
            bytearray([0x12, 0x00, 0x00]),

            # Unknown command
            bytearray([0xee, 0x00, 0x00]),

            # Change color to blue
            bytearray([0x20, 0x00, 0x03, 0x00, 0x00, 0xff]),

            # Change color to red
            bytearray([0x20, 0x00, 0x03, 0xff, 0x00, 0x00]),

            # Change color to green
            bytearray([0x20, 0x00, 0x03, 0x00, 0xff, 0x00]),
        ]

        for command in commands:
            self.transport.write(command)
            input('Press Enter to send next command')

    def connection_lost(self, exc):
        print('Lost connection of', self.peername)
        self.transport.close()


def main():
    loop = asyncio.get_event_loop()

    parser = argparse.ArgumentParser(description='Lantern TCP Server')
    parser.add_argument('host', type=str, default=HOST, nargs='?',
                        help='Server host, default is %(default)s')
    parser.add_argument('port', type=int, default=PORT, nargs='?',
                        help='Server port, default is %(default)s')
    args = parser.parse_args()

    coro = loop.create_server(LanternServerProtocol, args.host, args.port)
    server = loop.run_until_complete(coro)

    print('Serving on', server.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
