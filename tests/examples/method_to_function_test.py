# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import method_to_function
from undebt.pattern.interface import get_patterns
from undebt.pattern.testing import assert_transform


def test_simple():
    assert_transform(
        method_to_function,
        'id.method()',
        ['function(id)'],
    )


def test_actual_code():
    text = """
        if condition:
            # only when condition
            id = component.get(
                self.logic,
                id=id.method(),
            )
            ids = id.keys()
        else:
            if component.yes():
                ids = DO().get(
                    self.logic,
                    id=id.method(),
                )
            else:
                ids = component.get(
                    self.logic,
                    id=id.method(),
                )
    """
    assert_transform(
        method_to_function,
        text,
        [
            'function(id)',
            'function(id)',
            'function(id)',
        ],
    )


def test_object_id():
    assert_transform(
        method_to_function,
        "'id': ID(objs['id']).method()",
        ["function(ID(objs['id']))"],
    )


def test_no_self_dot():
    assert_transform(
        method_to_function,
        'self.method()',
        [],
    )


def test_method_to_function():
    patterns = get_patterns(method_to_function)
    text = """
obj.method().derp
"""
    assert process(patterns, text) == (
        """from function_lives_here import function

function(obj).derp
""")
