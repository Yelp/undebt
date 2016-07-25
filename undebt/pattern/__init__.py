# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import platform

from pyparsing import ParserElement


if platform.python_implementation() != "PyPy":
    ParserElement.enablePackrat()  # huge speedup in CPython, but can cause errors in PyPy

WHITESPACE_CHARS = " \t\f\v\r"
WHITESPACE_OR_NL_CHARS = WHITESPACE_CHARS + "\n"

# this must be called before any parsing is done
ParserElement.setDefaultWhitespaceChars(WHITESPACE_CHARS)
