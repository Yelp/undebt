# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import imp
import os
import re
import sys

from pyparsing import _trim_arity

from undebt.cmd.logger import log
from undebt.pattern.util import attach
from undebt.pattern.util import tokens_as_list


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
    from undebt.pattern.python import HEADER

    @tokens_as_list(assert_len=1)
    def extra_replace(tokens):
        if extra not in tokens[0]:
            return tokens[0] + extra + "\n"
        else:
            return None

    return HEADER, extra_replace


def patterns_from_files(pattern_files):
    """Returns patterns for pattern files."""
    return get_patterns(*(load_module(pattern_file) for pattern_file in pattern_files))


def load_module(path):
    """Loads a module from its path."""
    if module_like(path):
        return _load_module(path)

    pattern_name = os.path.splitext(os.path.basename(path))[0]
    return imp.load_source(pattern_name, path)


def _load_module(full_name):
    try:
        sys.path = [os.getcwd()] + sys.path
        (mod, path) = (None, None)
        for name in full_name.split('.'):
            # path=None defaults to sys.path (along with some other special
            # places), which is why we shim it to include the cwd.
            (f, p, d) = imp.find_module(name, path)
            mod = imp.load_module(name, f, p, d)
            # If `mod` is the final submodule, it will not have a __path__
            # attribute.
            path = getattr(mod, '__path__', None)

        return mod
    except ImportError as e:
        raise e
    finally:
        # Unshim path
        sys.path = sys.path[1:]


# _module_re is not _strictly_ correct, but we do a quick check for strings
# ending in .py before running the regex.
_module_re = re.compile(r'^\w+(\.\w+)*$')


def module_like(path):
    if path.endswith('.py'):
        return False

    return bool(_module_re.match(path))


def create_find_and_replace(grammar, replace):
    """Creates a find-and-replace grammar."""
    return attach(grammar, lambda s, l, t: [_trim_arity(replace)(s, l, t)])
