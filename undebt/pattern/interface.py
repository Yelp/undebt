# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from undebt.cmd.logger import log
from undebt.pattern.util import attach
from undebt.pattern.util import tokens_as_list
from undebt.pyparsing import _trim_arity


# required at the beginning of a string to be able to properly parse it
#  " " is necessary to make START_OF_FILE work properly
PARSING_PREFIX = " "


def parse_grammar(grammar, text):
    """Scan text and find matches for grammar."""
    formatted_text = PARSING_PREFIX + text
    results = grammar.parseWithTabs().scanString(formatted_text)
    return [(tokens, _fix_index(start), _fix_index(stop)) for tokens, start, stop in results]


def _fix_index(index):
    index -= len(PARSING_PREFIX)
    return index if index >= 0 else 0


def get_patterns(*pattern_modules):
    """Returns patterns for pattern modules."""
    return [_get_patterns(p) for p in pattern_modules]


def _get_patterns(pattern):
    if hasattr(pattern, "patterns"):
        return pattern.patterns

    if hasattr(pattern, "grammar") and hasattr(pattern, "replace"):
        patterns = [(pattern.grammar, pattern.replace)]
        if hasattr(pattern, "extra"):
            patterns.append(get_pattern_for_extra(pattern.extra))
        return patterns

    log.error(
        'pattern file {} must define either ("patterns") or ("grammar" and "replace" and optionally "extra")'
        .format(pattern.__name__)
    )
    sys.exit(1)


def get_pattern_for_extra(extra):
    """Returns a pattern object for an extra string."""
    from undebt.pattern.lang.python import HEADER

    @tokens_as_list(assert_len=1)
    def extra_replace(tokens):
        if extra not in tokens[0]:
            return tokens[0] + extra + "\n"
        else:
            return None

    return HEADER, extra_replace


def patterns_from_modules(pattern_modules):
    """Returns patterns for pattern files."""
    return get_patterns(*(load_module(pattern_module) for pattern_module in pattern_modules))


def load_module(module):
    """Loads a module from its name."""
    return __import__(module, fromlist=[''])


def create_find_and_replace(grammar, replace):
    """Creates a find-and-replace grammar."""
    return attach(grammar, lambda s, l, t: [_trim_arity(replace)(s, l, t)])
