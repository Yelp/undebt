# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path

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
    results = parse_grammar(pattern.grammar, text)
    assert len(results) == len(expected)
    assert expected == [pattern.replace(tokens) for tokens, _, _ in results]
