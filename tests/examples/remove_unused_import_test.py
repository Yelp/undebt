# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import remove_unused_import
from undebt.pattern.interface import get_patterns


def test_no_import():
    patterns = get_patterns(remove_unused_import)
    text = """
derp herp function(args) herp derp
"""
    assert process(patterns, text) == text


def test_function_used():
    patterns = get_patterns(remove_unused_import)
    text = """
from function_lives_here import function

derp herp function(args) herp derp
"""
    assert process(patterns, text) == text


def test_function_unused():
    patterns = get_patterns(remove_unused_import)
    text = """
from function_lives_here import function

derp herp herp derp
"""
    assert process(patterns, text) == (
        """

derp herp herp derp
""")
