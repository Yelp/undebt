# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import mock

from undebt.pattern.interface import _get_patterns


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
