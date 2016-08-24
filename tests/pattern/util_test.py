# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.testing import assert_parse
from undebt.pattern.util import in_string
from undebt.pattern.util import leading_whitespace
from undebt.pattern.util import quoted
from undebt.pattern.util import trailing_whitespace


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
