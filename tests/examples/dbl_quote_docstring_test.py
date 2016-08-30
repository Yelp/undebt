# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import dbl_quote_docstring
from undebt.pattern.interface import get_patterns
from undebt.pattern.testing import assert_transform


def test_actual_code():
    text = """
    def get(self):
        '''Returns a thing that does a thing because we really
        want to do that thing
        '''
        self.abcd.efgh('Do: {}'.format(
            self.opt.thing_to_do
        ))
        derp = []
    """
    assert_transform(
        dbl_quote_docstring,
        text,
        ['''"""Returns a thing that does a thing because we really
        want to do that thing
        """'''],
    )


def test_dbl_quote_docstring():
    patterns = get_patterns(dbl_quote_docstring)
    text = """
    def derp():
        '''doc'''
"""
    assert process(patterns, text) == ('''
    def derp():
        """doc"""
''')


def test_no_change():
    patterns = get_patterns(dbl_quote_docstring)
    text = """
    def derp():
        '''inside\"\"\"str'''
"""
    assert process(patterns, text) == (text)
