# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import attribute_to_function
from undebt.examples import method_to_function
from undebt.pattern.interface import get_patterns


def test_no_match():
    patterns = get_patterns(attribute_to_function)
    text = """
    derp.herp
    """
    assert process(patterns, text) == text


def test_match_method_but_not_import():
    patterns = get_patterns(method_to_function)
    text = """
from function_lives_here import function
obj.method().derp
"""
    assert process(patterns, text) == ("""
from function_lives_here import function
function(obj).derp
""")
