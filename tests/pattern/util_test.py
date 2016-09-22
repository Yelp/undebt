# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

import mock
from pyparsing import Keyword
from pyparsing import Literal

from undebt.pattern.testing import assert_parse
from undebt.pattern.util import debug
from undebt.pattern.util import in_string
from undebt.pattern.util import leading_whitespace
from undebt.pattern.util import quoted
from undebt.pattern.util import sequence
from undebt.pattern.util import trailing_whitespace


if sys.version_info.major == 3:
    builtin_module_name = 'builtins'
else:
    builtin_module_name = '__builtin__'


@mock.patch('{}.print'.format(builtin_module_name))
def test_debug(mock_print):
    assert_parse(
        grammar=debug(Keyword('something')),
        text="something",
        tokens_list=[
            [mock_print.return_value],
        ],
        interval_list=[
            (0, 9)
        ],
    )
    assert mock_print.call_count == 1


def test_quoted():
    assert_parse(
        grammar=quoted("derp"),
        text="""
        "derp"
        'herp'
        """,
        tokens_list=[
            ['"derp"'],
        ],
        interval_list=[
            (9, 15),
        ],
    )


def test_leading_whitespace():
    assert leading_whitespace("   a ") == "   "


def test_trailing_whitespace():
    assert trailing_whitespace(" a   ") == "   "


def test_in_string():
    test = "0123'567'9"
    assert not in_string(0, test)
    assert not in_string(1, test)
    assert not in_string(2, test)
    assert not in_string(3, test)
    assert not in_string(4, test)
    assert in_string(5, test)
    assert in_string(6, test)
    assert in_string(7, test)
    assert in_string(8, test)
    assert not in_string(9, test)


def test_sequence():
    a = Literal('a')
    double_a = sequence(a, n=2)
    triple_a = sequence(a, n=3)

    assert double_a.matches('aa')
    assert triple_a.matches('aaa')
    assert not double_a.matches('aaa')
    assert not triple_a.matches('aa')
