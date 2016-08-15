# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.interface import create_find_and_replace
from undebt.pattern.interface import parse_grammar


def assert_parse(grammar, text, tokens_list, interval_list):
    """Assert that grammar parses text to tokens_list on interval_list."""
    assert len(tokens_list) == len(interval_list)
    expected = [(tokens_list[i],) + interval_list[i] for i in range(len(tokens_list))]
    raw_assert_parse(grammar, text, expected)


def raw_assert_parse(grammar, text, token_interval_list):
    """Assert grammar parses text to expected tokens and intervals."""
    results = parse_grammar(grammar, text)
    assert len(results) == len(token_interval_list)
    assert token_interval_list == [(tokens.asList(), start, stop) for tokens, start, stop in results]


def assert_transform(pattern, text, transformed_tokens):
    """Assert grammar parses text to expected transformed tokens."""
    assert not hasattr(pattern, "patterns"), "assert_transform only works with basic style patterns"
    find_and_replace = create_find_and_replace(pattern.grammar, pattern.replace)
    results = parse_grammar(find_and_replace, text)
    assert len(results) == len(transformed_tokens)
    assert all(len(tokens) == 1 for tokens, _, _ in results)
    assert transformed_tokens == [tokens.asList()[0] for tokens, _, _ in results]
