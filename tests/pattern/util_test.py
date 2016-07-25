# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tests import assert_parse
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
