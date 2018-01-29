import os
import struct
import sys

import pytest

sys.path.insert(0, os.path.dirname('..'))

from lantern_tcp.utils import TCPClientProtocol


@pytest.mark.parametrize('tlv_input,output', [
    [[0x01, 0x00, 0x00], [(1, None)]],
    [[0xab, 0x00, 0x02, 0x10, 0x20], [(0xab, bytearray([0x10, 0x20]))]],
    [
        [0x01, 0x00, 0x00, 0xab, 0x00, 0x02, 0x10, 0x20],
        [(1, None), (0xab, bytearray([0x10, 0x20]))],
    ],
])
def test_parse_tlv_success(tlv_input, output):
    obj = TCPClientProtocol(None)
    assert list(obj.parse_tlv(bytearray(tlv_input))) == output


def test_parse_tlv_empty():
    obj = TCPClientProtocol(None)
    assert list(obj.parse_tlv(b'')) == []


def test_parse_tlv_broken():
    obj = TCPClientProtocol(None)
    assert list(obj.parse_tlv(bytearray([0xab, 0x00, 0x02, 0x10]))) == []
