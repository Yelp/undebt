# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import nl_at_eof
from undebt.pattern.interface import get_patterns
from undebt.pattern.testing import assert_transform


def test_match():
    assert_transform(
        nl_at_eof,
        'something',
        ['g\n'],
    )


def test_no_match():
    assert_transform(
        nl_at_eof,
        'something\n',
        [],
    )


def test_nl_at_eof():
    patterns = get_patterns(nl_at_eof)
    text = """
herp derp"""
    assert process(patterns, text) == ("""
herp derp
""")
