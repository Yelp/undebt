# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tests import assert_transform
from undebt.cmd.logic import process
from undebt.examples import exec_function
from undebt.pattern.interface import get_patterns


def test_globals():
    assert_transform(
        exec_function,
        'exec str in globals()',
        ['exec(str, globals())'],
    )


def test_globals_and_locals():
    assert_transform(
        exec_function,
        'exec str in globals(), locals()',
        ['exec(str, globals(), locals())'],
    )


def test_exec_function():
    patterns = get_patterns(exec_function)
    text = """
        exec stra in globals()
        exec strb in globals(), locals()
"""
    assert process(patterns, text) == ("""
        exec(stra, globals())
        exec(strb, globals(), locals())
""")
