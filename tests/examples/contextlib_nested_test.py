# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import contextlib_nested
from undebt.pattern.interface import get_patterns


def test_contextlib_nested():
    patterns = get_patterns(contextlib_nested)
    text = """
import mock
import contextlib
from contextlib import nested


with contextlib.nested(
        mock.patch(
            'os.path.join'),
        mock.patch('os.mkdir'),
        mock.patch('os.chdir'),
):
    pass


with nested(
        mock.patch(
            'os.path.join'
        ),
        mock.patch('os.mkdir'),
        mock.patch('os.chdir'),
):
    pass


def a_function():
    with contextlib.nested(
            mock.patch(
                'lots of stuff',
                'in this mock',
                return_value=None
            ), mock.patch(
                'reformatting really stinks'
            ),
    ):
        return None

with contextlib.nested(a, b, c) as (x, y, z):
    pass
"""
    assert process(patterns, text) == ("""
import mock
import contextlib
from contextlib import nested


with mock.patch(
            'os.path.join'), \\
    mock.patch('os.mkdir'), \\
    mock.patch('os.chdir'):
    pass


with mock.patch(
            'os.path.join'
        ), \\
    mock.patch('os.mkdir'), \\
    mock.patch('os.chdir'):
    pass


def a_function():
    with mock.patch(
                'lots of stuff',
                'in this mock',
                return_value=None
            ), \\
        mock.patch(
                'reformatting really stinks'
            ):
        return None

with a as x, \\
    b as y, \\
    c as z:
    pass
""")
