# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tests import assert_transform
from undebt.cmd.logic import process
from undebt.examples import hex_to_bitshift
from undebt.pattern.interface import get_patterns


def test_simple():
    assert_transform(
        hex_to_bitshift,
        'FLAGA=0x00000001',
        ['1 << 0'],
    )


def test_actual_code():
    text = """
        flags = bitfield_property(
            FLAGA=0x00000001,
            FLAGB=0x00000002,
            FLAGC=0x00000004,
            FLAGD=0x00000008,
            FLAGE=0x00000010,
            FLAGF=0x00000020,
            # comment
            FLAGG=0x00000040,
            FLAGH=0x00000080,
            FLAGI=0x00000100,
            # comment
            FLAGJ=0x00000200,
            FLAGK=0x00000400,
        )
    """
    assert_transform(
        hex_to_bitshift,
        text,
        [
            '1 << 0',
            '1 << 1',
            '1 << 2',
            '1 << 3',
            '1 << 4',
            '1 << 5',
            '1 << 6',
            '1 << 7',
            '1 << 8',
            '1 << 9',
            '1 << 10',
        ],
    )


def test_ignore_hex_not_power_of_two():
    assert_transform(
        hex_to_bitshift,
        'SOME_FLAG=0x123',
        [None],
    )


def test_avoid_negative_shift_count():
    assert_transform(
        hex_to_bitshift,
        'SOME_FLAG=0x0',
        [None],
    )


def test_hex_to_bitshift():
    patterns = get_patterns(hex_to_bitshift)
    text = """
0x001
0x002
0x003
0x004
"""
    assert process(patterns, text) == ("""
1 << 0
1 << 1
0x003
1 << 2
""")
