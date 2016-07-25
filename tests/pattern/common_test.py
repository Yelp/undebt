# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tests import assert_parse
from undebt.pattern.common import DOTTED_NAME
from undebt.pattern.common import INDENT
from undebt.pattern.common import NL_WHITE
from undebt.pattern.common import PARENS
from undebt.pattern.common import STRING
from undebt.pattern.common import WHITE


def test_INDENT():
    assert_parse(
        grammar=INDENT,
        text="""
        something
        """,
        tokens_list=[
            ["\n        "],
        ],
        interval_list=[
            (0, 9),
        ],
    )


def test_INDENT_START_OF_FILE():
    assert_parse(
        grammar=INDENT,
        text="    text",
        tokens_list=[
            [""],
        ],
        interval_list=[
            (4, 4)
        ],
    )


def test_WHITE():
    assert_parse(
        grammar=WHITE,
        text="""
        """,
        tokens_list=[
            ["        "],
        ],
        interval_list=[
            (1, 9),
        ],
    )


def test_NL_WHITE():
    assert_parse(
        grammar=NL_WHITE,
        text="""

        """,
        tokens_list=[
            ["\n        "],
        ],
        interval_list=[
            (1, 10),
        ],
    )


def test_STRING():
    assert_parse(
        grammar=STRING,
        text='''
        "derp"
        """
        herp
        """
        ''',
        tokens_list=[
            ['"derp"'],
            ['"""\n        herp\n        """'],
        ],
        interval_list=[
            (0, 15),
            (24, 52),
        ],
    )


def test_PARENS():
    assert_parse(
        grammar=PARENS,
        text="""
        (
        )(()
        )
        """,
        tokens_list=[
            ["(\n        )"],
            ["(()\n        )"],
        ],
        interval_list=[
            (9, 20),
            (20, 33),
        ],
    )


def test_DOTTED_NAME():
    assert_parse(
        grammar=DOTTED_NAME,
        text="""
        self.derp.herp
        """,
        tokens_list=[
            ["self.derp.herp"],
        ],
        interval_list=[
            (9, 23),
        ],
    )
