# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import class_inherit_object
from undebt.pattern.interface import get_patterns
from undebt.pattern.testing import assert_transform


def test_no_parens():
    assert_transform(
        class_inherit_object,
        'class derp:',
        ['class derp(object):'],
    )


def test_with_parens():
    assert_transform(
        class_inherit_object,
        'class herp():',
        ['class herp(object):'],
    )


def test_class_inherit_object():
    patterns = get_patterns(class_inherit_object)
    text = """
class derp: pass
class herp(): pass
"""
    assert process(patterns, text) == ("""
class derp(object): pass
class herp(object): pass
""")
