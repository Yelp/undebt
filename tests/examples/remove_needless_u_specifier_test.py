# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import remove_needless_u_specifier
from undebt.pattern.interface import get_patterns


def test_file_without_unicode_literals():
    patterns = get_patterns(remove_needless_u_specifier)
    text = """
from __future__ import print_statement, absolute_import

derp herp u"some string" herp derp
"""
    assert process(patterns, text) == text


def test_file_with_unicode_literals():
    patterns = get_patterns(remove_needless_u_specifier)
    text = """
from __future__ import unicode_literals

derp herp u"some string" herp derp
"""
    assert process(patterns, text) == (
        """
from __future__ import unicode_literals

derp herp "some string" herp derp
""")


def test_file_with_unicode_literals_and_others():
    patterns = get_patterns(remove_needless_u_specifier)
    text = """
from __future__ import print_statement, unicode_literals, absolute_import

derp herp u"some string" herp derp
"""
    assert process(patterns, text) == (
        """
from __future__ import print_statement, unicode_literals, absolute_import

derp herp "some string" herp derp
""")


def test_ignore_u_at_end_of_string():
    patterns = get_patterns(remove_needless_u_specifier)
    text = """
from __future__ import unicode_literals

subprocess.check_call(('mysql',
                       '-u', 'test_user',))
TITLE_LABELS = {
    "en": ("Subject", ),
    "ru": ("Тема", ),
    "fr": ("Objet", "Sujet"),
}
"""
    assert process(patterns, text) == text
