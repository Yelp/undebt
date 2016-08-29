# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import mock

from undebt.examples import attribute_to_function
from undebt.pattern.interface import get_patterns
from undebt.pattern.interface import module_like
from undebt.pattern.interface import module_name_to_path
from undebt.pattern.interface import _get_patterns
from undebt.pattern.python import HEADER


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


def test_module_like():
    assert module_like('foo.bar')
    assert module_like('foo.bar.baz')
    assert not module_like('foo/bar.py')
    assert not module_like('bar.py')


def test_module_name_to_path():
    assert module_name_to_path('foo') == 'foo.py'
    assert module_name_to_path('foo.bar') == 'foo/bar.py'
    assert module_name_to_path('foo.bar.baz') == 'foo/bar/baz.py'
