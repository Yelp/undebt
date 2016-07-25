# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tests import assert_transform
from undebt.cmd.logic import process
from undebt.examples import attribute_to_function
from undebt.pattern.interface import get_patterns


def test_simple():
    assert_transform(
        attribute_to_function,
        'obj.attribute',
        ['function(obj)'],
    )


def test_actual_code():
    text = """
        def somefunc(self):
            obj = something(self.attr).obj
            if obj is None:
                var = None
            else:
                var = self.attr.C.id(obj.attribute)['str']

            return self.x(
                abc=True,
                efg='str',
                hij='str',
                klm={
                    'str': str,
                },
            )
    """
    assert_transform(
        attribute_to_function,
        text,
        ['function(obj)'],
    )


def test_object_id():
    assert_transform(
        attribute_to_function,
        "'id': ID(obj['id']).attribute",
        ["function(ID(obj['id']))"],
    )


def test_more_dots():
    assert_transform(
        attribute_to_function,
        'self.id = o.id.attribute',
        ['function(o.id)'],
    )


def test_attribute_to_function():
    patterns = get_patterns(attribute_to_function)
    text = """
        obj.attribute
        h(obj.a.b(c).d[e].attribute)
"""
    assert process(patterns, text) == (
        """from function_lives_here import function

        function(obj)
        h(function(obj.a.b(c).d[e]))
""")
