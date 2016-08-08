# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path

from undebt.pattern.interface import create_find_and_replace
from undebt.pattern.interface import parse_grammar


tests_inputs_directory = os.path.join(os.path.dirname(__file__), "inputs")


def assert_parse(grammar, text, tokens_list, interval_list):
    assert len(tokens_list) == len(interval_list)
    expected = [(tokens_list[i],) + interval_list[i] for i in range(len(tokens_list))]
    raw_assert_parse(grammar, text, expected)


def raw_assert_parse(grammar, text, expected):
    results = parse_grammar(grammar, text)
    assert len(results) == len(expected)
    assert expected == [(tokens.asList(), start, stop) for tokens, start, stop in results]


def assert_transform(pattern, text, expected):
    assert not hasattr(pattern, "patterns"), "assert_transform only works with old/basic style patterns"
    find_and_replace = create_find_and_replace(pattern.grammar, pattern.replace)
    results = parse_grammar(find_and_replace, text)
    assert len(results) == len(expected)
    assert all(len(tokens) == 1 for tokens, _, _ in results)
    assert expected == [tokens.asList()[0] for tokens, _, _ in results]
