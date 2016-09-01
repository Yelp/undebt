# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.examples import deprecated_inequality_operator
from undebt.pattern.testing import assert_transform


def test_simple():
    assert_transform(
        deprecated_inequality_operator,
        '1 <> 2',
        ['1 != 2'],
    )


def test_actual_code():
    text = """
        def cold_war(self, foo, bar):
            if foo <> bar:
                launch_the_nukes()
    """
    assert_transform(
        deprecated_inequality_operator,
        text,
        ['foo != bar'],
    )
