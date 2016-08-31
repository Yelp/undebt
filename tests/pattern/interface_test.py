# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import mock
import pytest

from undebt.examples import attribute_to_function
from undebt.pattern.interface import get_patterns
from undebt.pattern.interface import load_module
from undebt.pattern.interface import maybe_path_to_module_name
from undebt.pattern.interface import _get_patterns
from undebt.pattern.lang.python import HEADER


def test_get_patterns_module_with_patterns():
    fake_pattern = mock.MagicMock()
    assert _get_patterns(fake_pattern) == fake_pattern.patterns


def test_get_patterns_module_with_grammar_and_replace():
    fake_pattern = mock.MagicMock()
    del fake_pattern.patterns
    del fake_pattern.extra
    assert _get_patterns(fake_pattern) == [(fake_pattern.grammar, fake_pattern.replace)]


@mock.patch('undebt.pattern.interface.log.error')
@mock.patch('undebt.pattern.interface.sys.exit')
def test_get_patterns_module_bad_format(mock_exit, mock_log):
    fake_pattern = mock.MagicMock()
    fake_pattern.__name__ = 'fake_pattern'
    del fake_pattern.patterns
    del fake_pattern.grammar

    _get_patterns(fake_pattern)

    assert mock_log.call_count == 1
    mock_exit.assert_called_once_with(1)


def test_get_patterns():
    # patterns = [[(grammar, replace), (HEADER, extra_replace)]]
    patterns = get_patterns(attribute_to_function)
    [patternset] = patterns
    [pattern1, pattern2] = patternset
    (grammar1, replace1) = pattern1
    (grammar2, replace2) = pattern2
    assert grammar2 is HEADER


def test_maybe_path_to_module_name():
    assert 'foo.bar' == maybe_path_to_module_name('foo.bar')
    assert 'foo.bar' == maybe_path_to_module_name('foo/bar.py')
    assert 'foo.bar' == maybe_path_to_module_name('foo/bar')

    with pytest.raises(ValueError):
        maybe_path_to_module_name('../relative/path.py')


def test_load_module_on_non_existant():
    with pytest.raises(ImportError):
        load_module('foo.bar.baz')
