# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.examples import swift
from undebt.pattern.testing import assert_transform


def test_one_liner():
    assert_transform(
        swift,
        'if let x = a where x == y {',
        ['if let x = a, x == y {'],
    )


def test_compound():
    text = 'if let x = a, y = b, z = c where x == y && y != z {'
    expected = 'if let x = a, let y = b, let z = c, x == y && y != z {'
    assert_transform(swift, text, [expected])


def test_expr():
    text = 'if let x = a + 1 / b where x == -y {'
    expected = 'if let x = a + 1 / b, x == -y {'
    assert_transform(swift, text, [expected])
