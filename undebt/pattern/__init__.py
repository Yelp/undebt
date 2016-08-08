# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import ParserElement


ParserElement.enablePackrat()

WHITESPACE_CHARS = " \t\f\v\r"
WHITESPACE_OR_NL_CHARS = WHITESPACE_CHARS + "\n"

# this must be called before any parsing is done,
# otherwise we won't be able to process whitespace correctly
ParserElement.setDefaultWhitespaceChars(WHITESPACE_CHARS)
