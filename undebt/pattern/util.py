# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import operator

from undebt.pattern import WHITESPACE_OR_NL_CHARS
from undebt.pyparsing import _trim_arity
from undebt.pyparsing import col
from undebt.pyparsing import Combine
from undebt.pyparsing import line
from undebt.pyparsing import originalTextFor
from undebt.pyparsing import replaceWith


def attach(item, action):
    """Attaches a parse action to an item."""
    return item.copy().addParseAction(action)


def fixto(item, output):
    """Forces an item to result in a specific output."""
    return attach(item, replaceWith(output))


def addspace(item):
    """Intersperses a space between auto-whitespace-parsed tokens."""
    return attach(item, " ".join)


def condense(item):
    """Condenses without space auto-whitespace-parsed tokens."""
    return attach(item, "".join)


def debug(item):
    """Modifies a grammar element to print whatever it matches."""
    return attach(item, lambda tokens: print(tokens))


def quoted(string):
    """Match a string containing the given string."""
    return originalTextFor(Combine("'" + string + "'") | Combine('"' + string + '"'))


def leading_whitespace(text):
    """Gets leading whitespace of text."""
    leading = ""
    while text and text[0] in WHITESPACE_OR_NL_CHARS:
        leading += text[0]
        text = text[1:]
    return leading


def trailing_whitespace(text):
    """Gets trailing whitespace of text."""
    trailing = ""
    while text and text[-1] in WHITESPACE_OR_NL_CHARS:
        trailing = text[-1] + trailing
        text = text[:-1]
    return trailing


def in_string(location, code):
    """Determines if the given location is in a string inside of code.

    Does not detect triple-quoted multi-line strings."""
    str_char = None
    for c in line(location, code)[:col(location, code) - 1]:
        if c == str_char:
            str_char = None
        elif c in "\"'":
            str_char = c
    return str_char is not None


def tokens_as_list(assert_len=None, assert_len_in=None):
    """Creates a decorator that passes tokens as a list."""
    def decorator(old_replace):
        @functools.wraps(old_replace)
        def new_replace(s, l, tokens):
            tokenlist = tokens.asList()
            if assert_len is not None:
                assert len(tokenlist) == assert_len, \
                    "len(" + repr(tokenlist) + ") != " + repr(assert_len)
            if assert_len_in is not None:
                assert len(tokenlist) in assert_len_in, "len(" + repr(tokenlist) + ") not in " + repr(assert_len_in)
            return _trim_arity(old_replace)(s, l, tokenlist)
        return new_replace
    return decorator


def tokens_as_dict(assert_keys=None, assert_keys_in=None):
    """Creates a decorator that passes tokens as a dict."""
    def decorator(old_replace):
        @functools.wraps(old_replace)
        def new_replace(s, l, tokens):
            tokendict = tokens.asDict()
            if assert_keys is not None:
                assert set(tokendict.keys()) >= set(assert_keys), \
                    repr(set(tokendict.keys())) + " != " + repr(set(assert_keys))
            if assert_keys_in is not None:
                assert set(tokendict.keys()) <= set(assert_keys_in), \
                    repr(set(tokendict.keys())) + " > " + repr(set(assert_keys_in))
            return _trim_arity(old_replace)(s, l, tokendict)
        return new_replace
    return decorator


def sequence(grammar, n):
    """
    Creates a grammar element that matches exactly N of the input
    grammar.
    """
    return functools.reduce(operator.add, [grammar] * n)
